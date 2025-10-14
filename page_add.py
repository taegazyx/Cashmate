# page_add.py (ฉบับแก้ไข)
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

# --- คลาส ExpenseDialog ไม่ต้องแก้ไขอะไรเลย เพราะใช้ callback อยู่แล้ว ---
class ExpenseDialog(ctk.CTkToplevel):
    """Custom dialog for adding expense amount and description."""
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

# --- Main Class for the Income/Expense Page ---
class AddPage:
    # <--- 1. แก้ไข __init__ ให้รับ main_app เข้ามา ---
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app # <--- เก็บตัวแปร main_app ไว้ใช้

        # <--- ลบการเก็บ state ของตัวเองออกไป ---
        # self.income_amount = 0
        # self.balance_amount = 0
        
        self.categories = [
            {"name": "Food", "label": "Food"},
            {"name": "Transport", "label": "Transport"},
            {"name": "Entertainment", "label": "Entertainment"},
            {"name": "Other", "label": "Other"}
        ]
        
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)
        self.frame.grid_columnconfigure(0, weight=1)

        self.setup_ui()
        self.update_display()

    # <--- 2. แก้ไข open_set_income_dialog ให้เรียก main_app ---
    def open_set_income_dialog(self, event=None):
        dialog = ctk.CTkInputDialog(text="Enter your income amount (THB):", title="Set Income")
        amount_str = dialog.get_input()
        try:
            amount = int(str(amount_str).replace(',', ''))
            if amount >= 0:
                # --- ส่งข้อมูลกลับไปที่ main_app ---
                self.main_app.set_income(amount)
            else:
                messagebox.showwarning("Input Error", "Income must be a positive number.")
        except (ValueError, TypeError):
            if amount_str is not None:
                messagebox.showwarning("Input Error", "Invalid input. Please enter numbers only.")

    # <--- 3. แก้ไข process_expense ให้เรียก main_app ---
    def process_expense(self, category, amount, description):
        # --- ส่งข้อมูลกลับไปที่ main_app ---
        self.main_app.add_expense(category, amount, description)

    def add_expense(self, category):
        ExpenseDialog(self.frame, category, self.process_expense)

    # <--- 4. แก้ไข update_display ให้ดึงข้อมูลจาก main_app ---
    def update_display(self):
        """Updates the labels by getting the latest data from main_app."""
        # --- ดึงข้อมูลล่าสุดจาก main_app มาแสดงผล ---
        income_display = f"{self.main_app.income:,.0f} THB"
        balance_display = f"{self.main_app.calculate_balance():,.0f} THB"
        
        if self.income_amount_label:
            self.income_amount_label.configure(text=income_display)
        if self.balance_amount_label:
            self.balance_amount_label.configure(text=balance_display)

    def setup_ui(self):
        # --- โค้ดส่วน UI ทั้งหมดเหมือนเดิม ไม่ต้องแก้ไข ---
        CARD_BG_COLOR = "#FFFFFF"
        BUTTON_COLOR = "#10B981"
        ACCENT_COLOR = "#059669"
        
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial Rounded MT Bold", 22)).pack()

        income_card_frame = ctk.CTkFrame(self.frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        income_card_frame.pack(fill="x")
        income_card_frame.bind("<Button-1>", self.open_set_income_dialog)
        
        income_card_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(income_card_frame, text="Income:", font=("Arial", 16)).grid(row=0, column=0, padx=20, sticky="w")
        self.income_amount_label = ctk.CTkLabel(income_card_frame, text="0 THB", font=("Arial Rounded MT Bold", 20))
        self.income_amount_label.grid(row=0, column=1, padx=20, sticky="e")

        scroll_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)
        scroll_frame.grid_columnconfigure((0,1), weight=1)

        for idx, cat in enumerate(self.categories):
            row, col = divmod(idx, 2)
            btn = ctk.CTkButton(scroll_frame, text=cat['label'], font=("Arial", 14), height=130, command=lambda c=cat["name"]: self.add_expense(c), fg_color=BUTTON_COLOR, hover_color=ACCENT_COLOR)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        balance_card_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color=CARD_BG_COLOR, height=80, border_color="#34D399", border_width=2)
        balance_card_frame.grid(row=(len(self.categories)//2), column=0, columnspan=2, pady=15, padx=10, sticky="ew")
        
        balance_card_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(balance_card_frame, text="Total Balance:", font=("Arial", 16)).grid(row=0, column=0, padx=20, sticky="w")
        self.balance_amount_label = ctk.CTkLabel(balance_card_frame, text="0 THB", font=("Arial Rounded MT Bold", 20))
        self.balance_amount_label.grid(row=0, column=1, padx=20, sticky="e")