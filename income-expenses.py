import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog
from datetime import date as dt 

# 🔴 IMPORT DatabaseManager
try:
    from database_manager import DatabaseManager
except ImportError:
    print("FATAL ERROR: Could not import 'database_manager.py'. โปรดตรวจสอบชื่อไฟล์")
    exit()

# 🟢 IMPORT NOTIFICATION FUNCTIONS
try:
    from finance_notifier import notify_expense, notify_income
    from CTkMessagebox import CTkMessagebox
except ImportError:
    print("⚠️ Warning: Could not import necessary modules. Notifications/Messagebox might be limited.")
    def notify_expense(*args, **kwargs): pass
    def notify_income(*args, **kwargs): pass
    try:
        from CTkMessagebox import CTkMessagebox
    except ImportError:
        # Dummy class หาก CTkMessagebox ไม่มี
        class CTkMessagebox:
            def __init__(self, **kwargs): print(f"Messagebox: {kwargs.get('message')}")

# ---------- กำหนดหมวดหมู่รายจ่าย ----------
categories = [
    {"name":"Food", "label":"อาหาร\nFood"},
    {"name":"Transport", "label":"เดินทาง\nTransport"},
    {"name":"Entertainment", "label":"ความบันเทิง\nEntertainment"},
    {"name":"Other", "label":"อื่นๆ\nOther"}
]

# ---------- Global References (สำหรับ update_display) ----------
income_amount_label = None
balance_amount_label = None
home_frame = None
profile_frame_container = None


# --- Custom Dialog for Adding Expense with Description ---
class ExpenseDialog(ctk.CTkToplevel):
    """Custom dialog for adding expense amount and description."""
    def __init__(self, master, category, callback):
        super().__init__(master)
        self.category = category
        self.callback = callback
        self.desc_entry = None
        self.title(f"เพิ่มรายการ: {category}")
        
        is_other = self.category == "Other"
        
        if is_other:
            self.geometry("400x320")
        else:
            self.geometry("400x250")

        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self, text=f"บันทึกรายจ่ายสำหรับ: {category}", font=("Arial Rounded MT Bold", 18), text_color="#064E3B").pack(pady=(15, 10))

        ctk.CTkLabel(self, text="1. จำนวนเงิน (Bath):", font=("Arial", 14), text_color="#34D399").pack(padx=20, anchor="w")
        self.amount_entry = ctk.CTkEntry(self, width=350, corner_radius=8, placeholder_text="กรอกจำนวนเงิน")
        self.amount_entry.pack(padx=20, fill="x")

        if is_other:
            ctk.CTkLabel(self, text="2. ชื่อรายการค่าใช้จ่าย (ระบุ):", font=("Arial", 14), text_color="#34D399").pack(padx=20, pady=(10, 0), anchor="w")
            self.desc_entry = ctk.CTkEntry(
                self, 
                width=350, 
                corner_radius=8, 
                placeholder_text="ระบุรายละเอียดรายการ (บังคับสำหรับ 'อื่นๆ')"
            )
            self.desc_entry.pack(padx=20, fill="x")

        pady_top = 20 if is_other else 30
        add_button = ctk.CTkButton(self, text="บันทึกรายการ", command=self.submit, fg_color="#10B981", hover_color="#059669")
        add_button.pack(pady=(pady_top, 10), padx=20, fill="x")
        
        self.amount_entry.focus_set()
        self.bind('<Escape>', lambda e: self.destroy())

    def submit(self):
        amount_str = self.amount_entry.get().replace(',', '')
        
        if self.category == "Other":
            description = self.desc_entry.get().strip()
            if not description:
                self.master.update_idletasks()
                CTkMessagebox(title="ข้อผิดพลาด", message="กรุณาระบุรายละเอียดรายการสำหรับหมวด 'อื่นๆ' ด้วย", icon="cancel")
                return
        else:
            description = self.category
        
        try:
            amount = float(amount_str) 
            if amount > 0:
                self.callback(self.category, amount, description) 
                self.destroy()
            else:
                self.master.update_idletasks() 
                CTkMessagebox(title="ข้อผิดพลาด", message="กรุณาใส่จำนวนเงินที่ถูกต้องและเป็นบวก", icon="cancel")
        except ValueError:
            self.master.update_idletasks() 
            CTkMessagebox(title="ข้อผิดพลาด", message="รูปแบบจำนวนเงินไม่ถูกต้อง", icon="cancel")
            self.amount_entry.delete(0, 'end')

# --- คลาสหลักของแอปพลิเคชัน ---

class CashMateApp(ctk.CTk):
    
    # --- 🔴 DATABASE CONFIGURATION ---
    DB_HOST = "127.0.0.1"
    DB_USER = "root"        # *** แก้ไข: ชื่อผู้ใช้ MariaDB ของคุณ ***
    DB_PASS = "25849"      # *** แก้ไข: รหัสผ่าน MariaDB ของคุณ ***
    DB_NAME = "cashmate_db"    # *** แก้ไข: ชื่อฐานข้อมูลของคุณ ***
    # ---------------------------------
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Initialize State Variables
        self.income_amount = 0.00
        self.balance_amount = 0.00
        self.current_page = "home"
        self.category_totals = {cat["name"]: 0.00 for cat in categories} 
        
        # 2. Connect Database
        self.db_manager = DatabaseManager(self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME)
        self.db_manager.connect() 
        
        # 3. Load Initial Data from DB
        self.load_initial_data()
        
        # 4. Setup UI
        self.setup_ui()
        
    def load_initial_data(self):
        """ดึงยอดรวมรายรับและยอดรวมรายจ่ายทั้งหมดจาก DB เพื่อคำนวณยอดคงเหลือเริ่มต้น"""
        
        total_income = self.db_manager.fetch_total_by_type("Income")
        total_expense = self.db_manager.fetch_total_by_type("Expense")
        
        db_category_totals = self.db_manager.fetch_category_totals()
        
        self.income_amount = total_income
        self.balance_amount = total_income - total_expense
        
        for cat_name in self.category_totals.keys():
            self.category_totals[cat_name] = db_category_totals.get(cat_name, 0.00)
        
    # --- Utility Methods ---
    
    def open_set_income_dialog(self):
        """Opens a dialog to set the initial income and calls notify_income."""
        dialog = ctk.CTkInputDialog(text="กรอกจำนวนรายรับ (Bath):", title="บันทึกรายรับ")
        amount_str = dialog.get_input()
        
        try:
            amount = float(str(amount_str).replace(',', '')) 
            if amount > 0:
                current_date = dt.today().isoformat()
                description = "รายรับใหม่"
                category = "General" 
                
                if self.db_manager.add_transaction("Income", category, description, amount, current_date):
                    
                    self.income_amount += amount
                    self.balance_amount += amount
                    self.update_display()
                    
                    notify_income(amount=amount, category=category, note=description, balance=self.balance_amount)
            else:
                CTkMessagebox(title="ข้อผิดพลาด", message="กรุณาใส่จำนวนเงินที่เป็นบวก", icon="cancel")
        except (ValueError, TypeError):
            if amount_str is not None:
                CTkMessagebox(title="ข้อผิดพลาด", message="รูปแบบจำนวนเงินไม่ถูกต้อง", icon="cancel")

    def process_expense(self, category, amount, description): 
        """Processes the expense data submitted and calls notify_expense."""
        
        current_date = dt.today().isoformat()
        if self.db_manager.add_transaction("Expense", category, description, amount, current_date):
            
            self.balance_amount -= amount
            self.category_totals[category] += amount # อัปเดตในหน่วยความจำ
            
            self.update_display()
            
            notify_expense(amount=amount, category=category, note=description, balance=self.balance_amount)

    def add_expense(self, category):
        """Opens a custom dialog to add expense amount and description."""
        ExpenseDialog(self, category, self.process_expense)

    def update_display(self):
        """Updates the labels for income and balance."""
        global income_amount_label, balance_amount_label
        
        income_display = f"{self.income_amount:,.0f} Bath"
        balance_display = f"{self.balance_amount:,.0f} Bath"
        
        if income_amount_label:
            income_amount_label.configure(text=income_display)
        if balance_amount_label:
            balance_amount_label.configure(text=balance_display)

    def update_profile_summary(self):
        """อัปเดตการแสดงผลสรุปในหน้า Profile"""
        
        # 1. ดึงข้อมูลล่าสุดจาก DB
        self.load_initial_data() 
        
        # 2. เคลียร์ UI Category Total Frame
        for widget in self.category_summary_frame.winfo_children():
            widget.destroy() 
            
        ctk.CTkLabel(self.category_summary_frame, text="ยอดรวมรายจ่ายแยกตามหมวดหมู่", font=("Arial Rounded MT Bold", 16), text_color="#064E3B").pack(pady=(15, 10))
        
        # 3. Loop แสดงผลแต่ละหมวดหมู่
        for cat in categories:
            cat_name = cat["name"]
            total = self.category_totals.get(cat_name, 0.00)
            
            summary_text = f"{cat['label'].split('\\n')[0]} ({cat_name}): {total:,.2f} Bath"
            
            ctk.CTkLabel(
                self.category_summary_frame, 
                text=summary_text, 
                font=("Arial", 14), 
                text_color="#059669",
                anchor="w",
                padx=15 
            ).pack(fill="x", pady=2, padx=30)
        
        # 4. แสดงยอดคงเหลือรวม
        ctk.CTkLabel(
            self.category_summary_frame, 
            text=f"\nยอดคงเหลือทั้งหมด: {self.balance_amount:,.2f} Bath", 
            font=("Arial Rounded MT Bold", 18), 
            text_color="#10B981"
        ).pack(pady=(10, 20))
        
    def on_closing(self):
        """ปิดการเชื่อมต่อฐานข้อมูลเมื่อปิดโปรแกรม"""
        self.db_manager.close()
        self.destroy()

    # --- UI Setup Methods ---

    def switch_page(self, target_page):
        """Switches the view between Home and Profile pages."""
        global home_frame, profile_frame_container
        
        if home_frame: home_frame.grid_forget()
        if profile_frame_container: profile_frame_container.grid_forget()
            
        if target_page == "home" and home_frame:
            home_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        elif target_page == "profile" and profile_frame_container:
            profile_frame_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.update_profile_summary()
    
    def safe_load_image(self, filepath, size):
        """Safely loads image, returns a CTkImage. On failure, returns a large red placeholder."""
        try:
            img_content = Image.open(filepath)
            return ctk.CTkImage(light_image=img_content, size=size)
        except FileNotFoundError:
            print(f"⚠️ Warning: Could not find image file: {filepath}. Using RED placeholder.")
            dummy_image = Image.new('RGB', size, color='red')
            return ctk.CTkImage(light_image=dummy_image, size=size) 

    def setup_ui(self):
        global income_amount_label, balance_amount_label, home_frame, profile_frame_container, main_content_frame

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # --- UI Constants ---
        CARD_BG_COLOR = "white"
        BUTTON_COLOR = "#10B981" 
        ACCENT_COLOR = "#059669" 
        BG_COLOR = "#C6F6D8" 

        self.title("CashMate App")
        self.configure(fg_color=BG_COLOR)
        self.geometry("900x600") 
        
        # --- Image Loading ---
        img_bank = self.safe_load_image("bank.png", size=(50, 50))
        img_income_icon = self.safe_load_image("income.png", size=(40, 40))
        img_balance_icon = self.safe_load_image("balance.png", size=(40, 40))
        img_profile_icon = self.safe_load_image("image_e3035c.png", size=(30, 30)) 
        
        icon_images = {
            "Food": self.safe_load_image("food.png", size=(60, 60)), 
            "Transport": self.safe_load_image("transport.png", size=(60, 60)),
            "Entertainment": self.safe_load_image("entertainment.png", size=(60, 60)),
            "Other": self.safe_load_image("other.png", size=(60, 60)),
        }

        # --- Main Content Centering Frame ---
        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.place(x=0, y=0, relwidth=1, relheight=1) 
        main_content_frame.grid_columnconfigure(0, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)
        
        # =================================================================
        # HOME PAGE UI
        # =================================================================

        home_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        home_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        home_frame.grid_columnconfigure(0, weight=1) 

        # --- Header Frame (Top Bar) ---
        header_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
        header_frame.pack(fill="x")

        top_bar_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_bar_frame.pack(fill="x")
        top_bar_frame.grid_columnconfigure(0, weight=1) 
        top_bar_frame.grid_columnconfigure(1, weight=1) 
        
        # Bank Icon
        bank_icon_label = ctk.CTkLabel(top_bar_frame, image=img_bank, text="", fg_color="transparent")
        bank_icon_label.grid(row=0, column=0, columnspan=2, pady=(5,0))
        
        # App Name
        ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial Rounded MT Bold", 22),
                      text_color="#064E3B", fg_color="transparent").pack(pady=(5, 15))


        # Profile Button
        profile_btn = ctk.CTkButton(
            top_bar_frame, 
            image=img_profile_icon, 
            text="", 
            width=30, 
            height=30, 
            fg_color="transparent", 
            hover_color="#A7F3D0",
            command=lambda: self.switch_page("profile") 
        )
        profile_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5) 


        # --- Income Card ---
        income_card_frame = ctk.CTkFrame(home_frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        income_card_frame.pack(pady=10, padx=0, fill="x")
        income_card_frame.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(income_card_frame, image=img_income_icon, text="", fg_color="transparent").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        ctk.CTkLabel(income_card_frame, text="รายรับ (Income) :", font=("Arial", 16), text_color="#10B981").grid(row=0, column=1, sticky="w")
        income_amount_label = ctk.CTkLabel(income_card_frame, text=" xxxx Bath", font=("Arial Rounded MT Bold", 20), text_color="#064E3B")
        income_amount_label.grid(row=0, column=1, sticky="e", padx=20) 

        income_card_frame.bind("<Button-1>", lambda event: self.open_set_income_dialog())


        # --- Scrollable Expenses (Category Buttons and Footer Content) ---
        scroll_frame = ctk.CTkScrollableFrame(home_frame, corner_radius=15, fg_color="transparent") 
        scroll_frame.pack(pady=10, padx=0, fill="both", expand=True) 
        scroll_frame.grid_columnconfigure((0,1), weight=1, uniform="group1")

        # 1. Category Buttons
        current_row = 0
        for idx, cat in enumerate(categories):
            row = idx // 2
            col = idx % 2
            
            btn = ctk.CTkButton(
                scroll_frame, 
                text=cat['label'], 
                image=icon_images.get(cat["name"]), 
                font=("Arial", 14), 
                height=130, 
                width=140, 
                compound="top", 
                command=lambda c=cat["name"]: self.add_expense(c), 
                fg_color=BUTTON_COLOR, 
                hover_color=ACCENT_COLOR, 
                text_color="white",
                corner_radius=15,
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            current_row = max(current_row, row)

        next_row = current_row + 1 

        # 2. Balance Card
        balance_card_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        balance_card_frame.grid(row=next_row, column=0, columnspan=2, pady=(15, 15), padx=10, sticky="ew")
        balance_card_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(balance_card_frame, image=img_balance_icon, text="", fg_color="transparent").grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        ctk.CTkLabel(balance_card_frame, text="ยอดคงเหลือ (Total Balance) :", font=("Arial", 16), text_color="#10B981").grid(row=0, column=1, sticky="w") 
        balance_amount_label = ctk.CTkLabel(balance_card_frame, text=" xxxx Bath", font=("Arial Rounded MT Bold", 20), text_color="#064E3B")
        balance_amount_label.grid(row=0, column=1, sticky="e", padx=20) 
        
        next_row += 1

        # =================================================================
        # PROFILE PAGE UI
        # =================================================================

        profile_frame_container = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        profile_frame_container.grid_columnconfigure(0, weight=1)
        profile_frame_container.grid_rowconfigure(0, weight=1)

        profile_inner_frame = ctk.CTkFrame(profile_frame_container, corner_radius=20, fg_color=CARD_BG_COLOR)
        profile_inner_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        profile_inner_frame.grid_columnconfigure(0, weight=1)

        # Profile Content Header
        ctk.CTkLabel(profile_inner_frame, image=img_profile_icon, text="", fg_color="transparent").pack(pady=(30, 10))
        ctk.CTkLabel(profile_inner_frame, text="Profile Settings", font=("Arial Rounded MT Bold", 24), text_color="#064E3B").pack(pady=(0, 5))
        ctk.CTkLabel(profile_inner_frame, text="จัดการข้อมูลส่วนตัวและการตั้งค่า", font=("Arial", 16), text_color="gray").pack(pady=(0, 30))

        # 🔴 Category Summary Frame (จะถูก populate ใน update_profile_summary)
        self.category_summary_frame = ctk.CTkFrame(
            profile_inner_frame, 
            corner_radius=10, 
            fg_color="#F0FFF4", 
            border_color="#34D399", 
            border_width=1
        )
        self.category_summary_frame.pack(pady=20, padx=30, fill="x")

        # Example Settings Buttons
        ctk.CTkButton(profile_inner_frame, text="Edit Name / Username", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
        ctk.CTkButton(profile_inner_frame, text="Change Password", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
        ctk.CTkButton(profile_inner_frame, text="App Theme (Light/Dark)", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
        ctk.CTkButton(profile_inner_frame, text="Export Data", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")

        # Back to Home Button
        ctk.CTkButton(profile_inner_frame, 
                      text="กลับสู่หน้าหลัก (Back to Home)", 
                      font=("Arial Rounded MT Bold", 18),
                      fg_color="#34D399", 
                      text_color="white", 
                      hover_color=ACCENT_COLOR,
                      height=50, 
                      corner_radius=10,
                      command=lambda: self.switch_page("home")
        ).pack(pady=(20, 30), padx=30, fill="x")


        # --- Initialization ---
        self.update_display() 
        self.switch_page("home") 
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

if __name__ == "__main__":
    app = CashMateApp()
    app.mainloop()