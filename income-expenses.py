import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog # ต้อง import filedialog เพื่อใช้ในการเลือกไฟล์รูปภาพ

# ---------- Global Variables ----------
income_amount = 0
balance_amount = 0
current_page = "home" # State variable for page switching

# ---------- กำหนดหมวดหมู่รายจ่าย ----------
categories = [
    {"name":"Food", "label":"อาหาร\nFood"},
    {"name":"Transport", "label":"เดินทาง\nTransport"},
    {"name":"Entertainment", "label":"ความบันเทิง\nEntertainment"},
    {"name":"Other", "label":"อื่นๆ\nOther"}
]

expenses = {cat["name"]:0 for cat in categories}

# Elements that need updating globally
income_amount_label = None
balance_amount_label = None
# Frames for switching pages
home_frame = None
profile_frame_container = None
main_content_frame = None
app = None
category_totals = {} # Dictionary to hold expense total labels
# 🌟 Global reference for background image to prevent garbage collection
bg_image_ref = None 

# --- Custom Dialog for Adding Expense with Description ---
class ExpenseDialog(ctk.CTkToplevel):
    """Custom dialog for adding expense amount and description."""
    def __init__(self, master, category, callback):
        super().__init__(master)
        self.category = category
        self.callback = callback
        self.desc_entry = None  # Initialize desc_entry
        self.title(f"เพิ่มรายการ: {category}")
        
        # Check if category is 'Other' to determine required fields and size
        is_other = self.category == "Other"
        
        if is_other:
            self.geometry("400x320") # Larger size for description input
        else:
            self.geometry("400x250") # Reduced size when description is not needed

        self.resizable(False, False)
        # Ensure the dialog stays on top
        self.attributes("-topmost", True)

        self.grid_columnconfigure(0, weight=1)
        
        # Title
        ctk.CTkLabel(self, text=f"บันทึกรายจ่ายสำหรับ: {category}", font=("Arial Rounded MT Bold", 18), text_color="#064E3B").pack(pady=(15, 10))

        # Amount Input
        ctk.CTkLabel(self, text="1. จำนวนเงิน (Bath):", font=("Arial", 14), text_color="#34D399").pack(padx=20, anchor="w")
        self.amount_entry = ctk.CTkEntry(self, width=350, corner_radius=8, placeholder_text="กรอกจำนวนเงิน")
        self.amount_entry.pack(padx=20, fill="x")

        # Description Input (Conditional - only for 'Other')
        if is_other:
            # 🟢 แสดงช่องใส่ชื่อรายการค่าใช้จ่ายเฉพาะหมวด 'อื่นๆ' เท่านั้น
            ctk.CTkLabel(self, text="2. ชื่อรายการค่าใช้จ่าย (ระบุ):", font=("Arial", 14), text_color="#34D399").pack(padx=20, pady=(10, 0), anchor="w")
            self.desc_entry = ctk.CTkEntry(
                self, 
                width=350, 
                corner_radius=8, 
                placeholder_text="ระบุรายละเอียดรายการ (บังคับสำหรับ 'อื่นๆ')"
            )
            self.desc_entry.pack(padx=20, fill="x")

        # Image Upload Section (Removed)
        # ctk.CTkLabel(self, text="3. รูปภาพ (Optional):", font=("Arial", 14), text_color="#34D399").pack(padx=20, pady=(10, 0), anchor="w")
        
        # image_frame = ctk.CTkFrame(self, fg_color="transparent")
        # image_frame.pack(padx=20, fill="x")
        # image_frame.grid_columnconfigure(0, weight=1)
        
        # self.image_path_label = ctk.CTkLabel(image_frame, text="ไม่มีไฟล์ที่เลือก", fg_color="#F3F4F6", text_color="#6B7280", corner_radius=5, wraplength=200)
        # self.image_path_label.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # self.choose_image_button = ctk.CTkButton(
        #     image_frame, 
        #     text="เลือกรูปภาพ", 
        #     command=self.choose_image, # Removed command
        #     fg_color="#34D399", 
        #     hover_color="#059669", 
        #     width=100
        # )
        # self.choose_image_button.grid(row=0, column=1, sticky="e")

        # Add Button
        # 📌 ปรับ padding ตามความเหมาะสมเมื่อมี/ไม่มีช่อง Description
        pady_top = 20 if is_other else 30
        add_button = ctk.CTkButton(self, text="บันทึกรายการ", command=self.submit, fg_color="#10B981", hover_color="#059669")
        add_button.pack(pady=(pady_top, 10), padx=20, fill="x")
        
        # Set focus to amount entry
        self.amount_entry.focus_set()

        # Bind Esc key to close
        self.bind('<Escape>', lambda e: self.destroy())

    # Removed choose_image method
    # def choose_image(self):
    #     """Opens file dialog to select an image file."""
    #     ...

    def submit(self):
        amount_str = self.amount_entry.get().replace(',', '')
        
        # 📌 ตรวจสอบและกำหนดค่า Description ตามเงื่อนไข
        if self.category == "Other":
            # สำหรับหมวด 'อื่นๆ' ต้องดึงค่าจาก entry และต้องไม่ว่างเปล่า
            description = self.desc_entry.get().strip()
            if not description:
                self.master.update_idletasks()
                # Use CTkMessagebox for custom error display
                ctk.CTkMessagebox(title="ข้อผิดพลาด", message="กรุณาระบุรายละเอียดรายการสำหรับหมวด 'อื่นๆ' ด้วย", icon="cancel")
                return
        else:
            # สำหรับหมวดอื่นๆ ให้ใช้ชื่อหมวดหมู่เป็น description โดยอัตโนมัติ
            description = self.category
        
        try:
            # Validate amount input
            amount = int(amount_str)
            if amount > 0:
                # Pass amount, category, description back to the main app
                self.callback(self.category, amount, description) 
                self.destroy()
            else:
                print("❌ จำนวนเงินต้องเป็นจำนวนเต็มบวก")
                # Use a custom message box instead of printing to console for user visibility
                self.master.update_idletasks() # Ensure UI is updated before showing next dialog
                ctk.CTkMessagebox(title="ข้อผิดพลาด", message="กรุณาใส่จำนวนเงินที่ถูกต้องและเป็นบวก", icon="cancel")
        except ValueError:
            print("❌ กรุณากรอกจำนวนเงินที่ถูกต้อง")
            self.master.update_idletasks() 
            ctk.CTkMessagebox(title="ข้อผิดพลาด", message="รูปแบบจำนวนเงินไม่ถูกต้อง", icon="cancel")
            self.amount_entry.delete(0, 'end')

# --- Utility Functions ---

def open_set_income_dialog():
    """Opens a dialog to set the initial income."""
    global income_amount, balance_amount
    dialog = ctk.CTkInputDialog(text="กรอกจำนวนรายรับ (Bath):", title="บันทึกรายรับ")
    amount_str = dialog.get_input()
    
    try:
        # Use str(amount_str).replace(',', '') to handle potential existing comma formatting
        amount = int(str(amount_str).replace(',', '')) 
        if amount >= 0:
            income_amount = amount
            balance_amount = amount
            update_display()
        else:
            print("❌ กรุณากรอกตัวเลขรายรับที่เป็นบวก")
    except (ValueError, TypeError):
        print("❌ ไม่ได้กรอกจำนวนเงินที่ถูกต้อง")

def process_expense(category, amount, description): # Removed image_path parameter
    """Processes the expense data submitted from the dialog."""
    global balance_amount
    balance_amount -= amount
    expenses[category] += amount
    
    # Log all captured data (description is now guaranteed)
    print(f"✅ บันทึกรายจ่าย: {amount} บาท | หมวดหมู่: {category} | ชื่อรายการ: {description}") 
    
    update_display()
    # In a real app, this should update the transaction list, but since we only display category totals:
    # We update the total here for visual confirmation (if implemented).
    # if category in category_totals:
    #      category_totals[category].configure(text=f"รวม: {expenses[category]:,.0f} บาท")


def add_expense(category):
    """Opens a custom dialog to add expense amount and description."""
    # Pass the main app instance and the callback function
    ExpenseDialog(app, category, process_expense)

def update_display():
    """Updates the labels for income and balance."""
    # Use locale-aware formatting for currency display (adding commas)
    income_display = f"{income_amount:,.0f} Bath"
    balance_display = f"{balance_amount:,.0f} Bath"
    
    if income_amount_label:
        income_amount_label.configure(text=income_display)
    if balance_amount_label:
        balance_amount_label.configure(text=balance_display)

def switch_page(target_page):
    """Switches the view between Home and Profile pages."""
    global current_page
    current_page = target_page
    
    # Hide all main page containers
    if home_frame:
        home_frame.grid_forget()
    if profile_frame_container:
        profile_frame_container.grid_forget()
        
    # Show the target page container
    if target_page == "home" and home_frame:
        home_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    elif target_page == "profile" and profile_frame_container:
        profile_frame_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


# --- Image Loading ---
def safe_load_image(filepath, size):
    """Safely loads image, returns a CTkImage. On failure, returns a large red placeholder."""
    try:
        img_content = Image.open(filepath)
        return ctk.CTkImage(light_image=img_content, size=size)
    except FileNotFoundError:
        print(f"⚠️ Warning: Could not find image file: {filepath}. Using RED placeholder.")
        # หากโหลดไม่ได้ ให้สร้างรูปสีแดงขนาดเท่าเดิมแทน เพื่อตรวจสอบว่าวางตำแหน่งถูกหรือไม่
        dummy_image = Image.new('RGB', size, color='red')
        return ctk.CTkImage(light_image=dummy_image, size=size) 

def setup_ui():
    global app, income_amount_label, balance_amount_label, home_frame, profile_frame_container, main_content_frame, bg_image_ref

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    
    # --- UI Constants ---
    CARD_BG_COLOR = "white"
    BUTTON_COLOR = "#10B981" # Green
    ACCENT_COLOR = "#059669" # Darker Green
    BG_COLOR = "#C6F6D8" # 🌟 สีพื้นหลังเป็นสีเขียวอ่อน

    app = ctk.CTk()
    app.title("CashMate App")
    # 🌟 กำหนดสีพื้นหลังหลักของแอป
    app.configure(fg_color=BG_COLOR)
    # 🌟 ขนาดหน้าจอ 900x600
    app.geometry("900x600") 
    
    # --- Image Loading ---
    img_bank = safe_load_image("bank.png", size=(50, 50))
    img_income_icon = safe_load_image("income.png", size=(40, 40))
    img_balance_icon = safe_load_image("balance.png", size=(40, 40))
    img_profile_icon = safe_load_image("image_e3035c.png", size=(30, 30)) 
    
    icon_images = {
        # 🟢 ถูกแก้ไขเป็น food.png ในการตอบกลับครั้งก่อน
        "Food": safe_load_image("food.png", size=(60, 60)), 
        "Transport": safe_load_image("transport.png", size=(60, 60)),
        "Entertainment": safe_load_image("entertainment.png", size=(60, 60)),
        "Other": safe_load_image("other.png", size=(60, 60)),
    }

    # 🌟 --- Main Content Centering Frame ---
    main_content_frame = ctk.CTkFrame(app, fg_color="transparent")
    main_content_frame.place(x=0, y=0, relwidth=1, relheight=1) 
    main_content_frame.grid_columnconfigure(0, weight=1)
    main_content_frame.grid_rowconfigure(0, weight=1)
    
    # =================================================================
    # HOME PAGE UI (Active Page)
    # =================================================================

    home_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
    home_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    home_frame.grid_columnconfigure(0, weight=1) # Center content horizontally

    # --- Header Frame (Top Bar) inside home_frame ---
    header_frame = ctk.CTkFrame(home_frame, fg_color="transparent")
    header_frame.pack(fill="x")

    top_bar_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    top_bar_frame.pack(fill="x")
    top_bar_frame.grid_columnconfigure(0, weight=1) 
    top_bar_frame.grid_columnconfigure(1, weight=1) 
    
    # Bank Icon (Center-top)
    bank_icon_label = ctk.CTkLabel(top_bar_frame, image=img_bank, text="", fg_color="transparent")
    bank_icon_label.grid(row=0, column=0, columnspan=2, pady=(5,0))
    
    # App Name (Below Bank Icon)
    ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial Rounded MT Bold", 22),
                 text_color="#064E3B", fg_color="transparent").pack(pady=(5, 15))


    # Profile Button Placeholder (Top Right corner) 
    profile_btn = ctk.CTkButton(
        top_bar_frame, 
        image=img_profile_icon, 
        text="", # ⚙️ แก้ไข: ลบข้อความ "..." ออก ให้เหลือแต่ไอคอน
        width=30, 
        height=30, 
        # compound="right", # ไม่จำเป็นต้องใช้ compound เมื่อไม่มีข้อความ
        fg_color="transparent", 
        hover_color="#A7F3D0",
        command=lambda: switch_page("profile") # เพิ่มคำสั่งสลับหน้า
    )
    profile_btn.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5) 


    # --- Income Card (Display) ---
    income_card_frame = ctk.CTkFrame(home_frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
    income_card_frame.pack(pady=10, padx=0, fill="x")
    income_card_frame.grid_columnconfigure(1, weight=1) 

    ctk.CTkLabel(income_card_frame, image=img_income_icon, text="", fg_color="transparent").grid(row=0, column=0, padx=15, pady=15, sticky="w")
    
    ctk.CTkLabel(income_card_frame, text="รายรับ (Income) :", font=("Arial", 16), text_color="#10B981").grid(row=0, column=1, sticky="w")
    income_amount_label = ctk.CTkLabel(income_card_frame, text=" xxxx Bath", font=("Arial Rounded MT Bold", 20), text_color="#064E3B")
    income_amount_label.grid(row=0, column=1, sticky="e", padx=20) 

    income_card_frame.bind("<Button-1>", lambda event: open_set_income_dialog())


    # --- Scrollable Expenses (Category Buttons and Footer Content) ---
    scroll_frame = ctk.CTkScrollableFrame(home_frame, corner_radius=15, fg_color="transparent") 
    scroll_frame.pack(pady=10, padx=0, fill="both", expand=True) 
    scroll_frame.grid_columnconfigure((0,1), weight=1, uniform="group1")

    # 1. Category Buttons (ใช้ grid)
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
            # 🌟 UPDATED: Call add_expense which now opens the custom dialog
            command=lambda c=cat["name"]: add_expense(c), 
            fg_color=BUTTON_COLOR,       
            hover_color=ACCENT_COLOR,    
            text_color="white",
            corner_radius=15,
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        current_row = max(current_row, row)

    next_row = current_row + 1 

    # 2. Balance Card (ใช้ grid)
    # --- Balance Card (Display) ---
    balance_card_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
    balance_card_frame.grid(row=next_row, column=0, columnspan=2, pady=(15, 15), padx=10, sticky="ew")
    balance_card_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(balance_card_frame, image=img_balance_icon, text="", fg_color="transparent").grid(row=0, column=0, padx=15, pady=15, sticky="w")
    
    ctk.CTkLabel(balance_card_frame, text="ยอดคงเหลือ (Total Balance) :", font=("Arial", 16), text_color="#10B981").grid(row=0, column=1, sticky="w") 
    balance_amount_label = ctk.CTkLabel(balance_card_frame, text=" xxxx Bath", font=("Arial Rounded MT Bold", 20), text_color="#064E3B")
    balance_amount_label.grid(row=0, column=1, sticky="e", padx=20) 
    
    next_row += 1

    # 📌 ลบปุ่ม "Back to Home" ที่ซ้ำซ้อนออกจาก Home Page (Footer)
    # next_row += 1


    # =================================================================
    # PROFILE PAGE UI (Kept definition but not functional)
    # =================================================================

    # Create a main container for the Profile Page (initially hidden)
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

    # Example Settings Buttons (Kept for UI completeness)
    ctk.CTkButton(profile_inner_frame, text="Edit Name / Username", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
    ctk.CTkButton(profile_inner_frame, text="Change Password", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
    ctk.CTkButton(profile_inner_frame, text="App Theme (Light/Dark)", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")
    ctk.CTkButton(profile_inner_frame, text="Export Data", fg_color=BUTTON_COLOR, text_color="white", height=45, corner_radius=10).pack(pady=10, padx=30, fill="x")

    # 🟢 เพิ่มปุ่ม "Back to Home" ที่นี่เพื่อให้ผู้ใช้กลับไปยังหน้าหลักได้จากหน้าโปรไฟล์
    ctk.CTkButton(profile_inner_frame, 
                  text="กลับสู่หน้าหลัก (Back to Home)", 
                  font=("Arial Rounded MT Bold", 18),
                  fg_color="#34D399", 
                  text_color="white", 
                  hover_color=ACCENT_COLOR,
                  height=50, 
                  corner_radius=10,
                  command=lambda: switch_page("home")
    ).pack(pady=(20, 30), padx=30, fill="x")


    # --- Initialization ---
    update_display() 
    switch_page("home") # Ensure Home page is shown first and other frames are hidden

    # ---------- Run ----------
    app.mainloop()

if __name__ == "__main__":
    setup_ui()
