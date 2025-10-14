# page_add.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# --- คลาส ExpenseDialog (เหมือนเดิม ไม่ต้องแก้ไข) ---
class ExpenseDialog(ctk.CTkToplevel):
    # ... (โค้ดส่วนนี้ถูกต้องอยู่แล้ว) ...
    def __init__(self, master, category, callback):
        super().__init__(master)
        self.category = category
        self.callback = callback
        self.desc_entry = None
        self.title(f"Add Entry: {category}")
        is_other = self.category == "Other"
        self.geometry("400x320" if is_other else "400x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        ctk.CTkLabel(self, text=f"Log expense for: {category}", font=("Arial Rounded MT Bold", 18)).pack(pady=(15, 10))
        ctk.CTkLabel(self, text="1. Amount (THB):", font=("Arial", 14)).pack(padx=20, anchor="w")
        self.amount_entry = ctk.CTkEntry(self, width=350, placeholder_text="Enter amount")
        self.amount_entry.pack(padx=20, fill="x")
        if is_other:
            ctk.CTkLabel(self, text="2. Expense Name:", font=("Arial", 14)).pack(padx=20, pady=(10, 0), anchor="w")
            self.desc_entry = ctk.CTkEntry(self, width=350, placeholder_text="Specify item (required for 'Other')")
            self.desc_entry.pack(padx=20, fill="x")
        pady_top = 20 if is_other else 30
        add_button = ctk.CTkButton(self, text="Save Entry", command=self.submit)
        add_button.pack(pady=(pady_top, 10), padx=20, fill="x")
        self.amount_entry.focus_set()
        self.bind('<Escape>', lambda e: self.destroy())

    def submit(self):
        amount_str = self.amount_entry.get().replace(',', '')
        description = self.category
        if self.category == "Other":
            description = self.desc_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Please specify the item name for the 'Other' category.")
                return
        try:
            amount = int(amount_str)
            if amount > 0:
                self.callback(self.category, amount, description) 
                self.destroy()
            else:
                messagebox.showerror("Error", "Please enter a positive number for the amount.")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount format. Please enter numbers only.")
            self.amount_entry.delete(0, 'end')


# --- คลาสหลักสำหรับหน้า Add Income/Expense ---
class AddPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app 
        
        # --- ค่าคงที่สำหรับ UI ---
        self.CARD_BG_COLOR = "#FFFFFF"
        self.BUTTON_COLOR = "#10B981"
        self.ACCENT_COLOR = "#059669"
        
        self.categories = [
            {"name": "Food", "label": "Food"},
            {"name": "Transport", "label": "Transport"},
            {"name": "Entertainment", "label": "Entertainment"},
            {"name": "Other", "label": "Other"}
        ]
        
        # <--- 1. โหลดรูปภาพทั้งหมดที่ต้องใช้ ---
        self.load_images()
        
        self.frame = ctk.CTkFrame(parent, fg_color="#C6F6D8")
        self.frame.pack(fill="both", expand=True)
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.update_display()

    # <--- 2. เพิ่มเมธอดสำหรับโหลดรูปภาพ ---
    def _safe_load_image(self, filepath, size):
        """Safely loads an image and returns a CTkImage, or a placeholder on failure."""
        try:
            img_content = Image.open(filepath)
            return ctk.CTkImage(light_image=img_content, size=size)
        except FileNotFoundError:
            print(f"⚠️ Warning: Image not found at '{filepath}'. Using a red placeholder.")
            dummy_image = Image.new('RGB', size, color='red')
            return ctk.CTkImage(light_image=dummy_image, size=size)
            
    def load_images(self):
        """Loads all necessary images for the UI."""
        self.icon_images = {
            "Food": self._safe_load_image("food.png", size=(60, 60)), 
            "Transport": self._safe_load_image("transport.png", size=(60, 60)),
            "Entertainment": self._safe_load_image("entertainment.png", size=(60, 60)),
            "Other": self._safe_load_image("other.png", size=(60, 60)),
        }

    # --- เมธอดอื่นๆ (เหมือนเดิม) ---
    def open_set_income_dialog(self, event=None):
        # ... (โค้ดส่วนนี้เหมือนเดิม) ...
        dialog = ctk.CTkInputDialog(text="Enter your income amount (THB):", title="Set Income")
        amount_str = dialog.get_input()
        try:
            amount = int(str(amount_str).replace(',', ''))
            if amount >= 0:
                self.main_app.set_income(amount)
            else:
                messagebox.showwarning("Input Error", "Income must be a positive number.")
        except (ValueError, TypeError):
            if amount_str is not None:
                messagebox.showwarning("Input Error", "Invalid input. Please enter numbers only.")

    def process_expense(self, category, amount, description):
        self.main_app.add_expense(category, amount, description)

    def add_expense(self, category):
        ExpenseDialog(self.frame, category, self.process_expense)

    def update_display(self):
        income_display = f"{self.main_app.income:,.0f} THB"
        balance_display = f"{self.main_app.calculate_balance():,.0f} THB"
        if hasattr(self, 'income_amount_label'): self.income_amount_label.configure(text=income_display)
        if hasattr(self, 'balance_amount_label'): self.balance_amount_label.configure(text=balance_display)

    def setup_ui(self):
        # --- Header ---
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(15, 15))
        ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial Rounded MT Bold", 22)).pack()

        # --- Income Card ---
        income_card_frame = ctk.CTkFrame(self.frame, corner_radius=15, fg_color=self.CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        income_card_frame.pack(fill="x", padx=20)
        income_card_frame.bind("<Button-1>", self.open_set_income_dialog)
        income_card_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(income_card_frame, text="Income:", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.income_amount_label = ctk.CTkLabel(income_card_frame, text="0 THB", font=("Arial Rounded MT Bold", 20))
        self.income_amount_label.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        # --- Scrollable Area ---
        scroll_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        scroll_frame.grid_columnconfigure((0,1), weight=1)

        # --- Category Buttons ---
        for idx, cat in enumerate(self.categories):
            row, col = divmod(idx, 2)
            btn = ctk.CTkButton(
                scroll_frame, 
                text=cat['label'], 
                # <--- 3. นำรูปภาพที่โหลดไว้มาใช้งาน ---
                image=self.icon_images.get(cat["name"]),
                compound="top", # ทำให้รูปอยู่บนข้อความ
                font=("Arial", 14), 
                height=130, 
                command=lambda c=cat["name"]: self.add_expense(c), 
                fg_color=self.BUTTON_COLOR,
                hover_color=self.ACCENT_COLOR
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # --- Balance Card ---
        balance_card_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color=self.CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        balance_card_frame.grid(row=(len(self.categories)//2), column=0, columnspan=2, pady=15, padx=10, sticky="ew")
        balance_card_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(balance_card_frame, text="Total Balance:", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.balance_amount_label = ctk.CTkLabel(balance_card_frame, text="0 THB", font=("Arial Rounded MT Bold", 20))
        self.balance_amount_label.grid(row=0, column=1, padx=20, pady=20, sticky="e")