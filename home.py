# main_app.py (ฉบับสมบูรณ์)
import customtkinter as ctk
from tkinter import messagebox

# --- Import ทุกหน้าที่จำเป็น ---
from page_history import HistoryPage
from page_profile import ProfilePage
from page_add import AddPage
from page_dashboard import DashboardPage

# --- Import ฟังก์ชันแจ้งเตือนเข้ามา ---
from finance_notifier import notify_income, notify_expense

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.resizable(0, 0)
        self.title("CASHMATH")

        # --- "ฐานข้อมูลชั่วคราว" ในแอป ---
        # self.income = 0.0 # <--- เราจะไม่ใช้ตัวแปรนี้แล้ว
        self.transactions = [] # <--- เก็บทุกอย่างทั้งรายรับและรายจ่าย

        self.create_main_app_view()

    def add_expense(self, category, amount, description):
        """เมธอดสำหรับเพิ่มรายจ่าย"""
        transaction_data = {
            "type": "Expense", # <--- เพิ่มประเภท
            "category": category,
            "amount": float(amount),
            "desc": description
        }
        self.transactions.append(transaction_data)
        
        # --- ยิงแจ้งเตือนหลังจากบันทึก (ส่ง description ไปเป็น note) ---
        current_balance = self.calculate_balance()
        notify_expense(
            amount=float(amount), 
            category=category, 
            note=description, # <--- ส่ง description ไปด้วย
            balance=current_balance
        )
        
        self.create_main_app_view()

    # <--- เปลี่ยนจาก set_income เป็น add_income ---
    def add_income(self, amount, description="Income"):
        """เมธอดสำหรับเพิ่มรายรับ"""
        transaction_data = {
            "type": "Income", # <--- เพิ่มประเภท
            "category": "Income", # กำหนดหมวดหมู่พื้นฐาน
            "amount": float(amount),
            "desc": description
        }
        self.transactions.append(transaction_data)

        # --- ยิงแจ้งเตือนหลังจากบันทึก ---
        current_balance = self.calculate_balance()
        notify_income(amount=float(amount), balance=current_balance)
        
        self.create_main_app_view()

    # <--- แก้ไข calculate_balance ให้คำนวณจาก list ทั้งหมด ---
    def calculate_balance(self):
        """คำนวณยอดคงเหลือจาก transactions ทั้งหมด"""
        total_income = sum(t['amount'] for t in self.transactions if t.get('type') == 'Income')
        total_expense = sum(t['amount'] for t in self.transactions if t.get('type') == 'Expense')
        return total_income - total_expense

    def get_recent_transactions(self, count=5):
        return self.transactions[-count:]

    def load_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if page_name == "Dashboard Home":
            DashboardPage(parent=self.content_frame, main_app=self)
        elif page_name == "Add Income/Expense":
            AddPage(parent=self.content_frame, main_app=self)
        elif page_name == "History":
            HistoryPage(parent=self.content_frame, main_app=self)
        elif page_name == "Profile":
            ProfilePage(parent=self.content_frame, main_app=self)

    def create_main_app_view(self):
        for widget in self.winfo_children():
            widget.destroy()

        dashboard_frame = ctk.CTkFrame(self, fg_color="#F8F8FF")
        dashboard_frame.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(dashboard_frame, width=200, fg_color="#601E88")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="☰ Menu", font=("Arial Bold", 18), text_color="white").pack(pady=20)

        self.content_frame = ctk.CTkFrame(dashboard_frame, fg_color="#F8F8FF")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        menu_items = [
            ("🏠 Dashboard", "Dashboard Home"),
            ("➕ Add Income/Expense", "Add Income/Expense"),
            ("📜 History", "History"),
            ("👤 Profile", "Profile"),
        ]

        for text, page in menu_items:
            ctk.CTkButton(sidebar, text=text, fg_color="#7733AA", hover_color="#9955CC",
                          command=lambda p=page: self.load_page(p)).pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(sidebar, text="🚪 Exit", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.quit_app).pack(fill="x", side="bottom", pady=20, padx=10)

        self.load_page("Dashboard Home")

    def quit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()