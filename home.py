# main_app.py (ฉบับสมบูรณ์พร้อมระบบแจ้งเตือน)
import customtkinter as ctk
from tkinter import messagebox

# --- Import ทุกหน้าที่จำเป็น ---
from page_history import HistoryPage
from page_profile import ProfilePage
from page_add import AddPage
from page_dashboard import DashboardPage

# <--- 1. Import ฟังก์ชันแจ้งเตือนเข้ามา ---
from finance_notifier import notify_income, notify_expense

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.resizable(0, 0)
        self.title("CASHMATH")
        self.income = 0.0
        self.transactions = []
        self.create_main_app_view()

    def add_expense(self, category, amount, description):
        """เมธอดสำหรับเพิ่มรายจ่าย"""
        transaction_data = {"category": category, "amount": float(amount), "desc": description}
        self.transactions.append(transaction_data)
        
        # <--- 2. ยิงแจ้งเตือนหลังจากบันทึกข้อมูล! ---
        current_balance = self.calculate_balance()
        notify_expense(amount=float(amount), category=category, balance=current_balance)

        # รีเฟรชหน้าจอ (เหมือนเดิม)
        self.create_main_app_view()

    def set_income(self, amount):
        """เมธอดสำหรับตั้งค่ารายรับ"""
        self.income = float(amount)

        # <--- 3. ยิงแจ้งเตือนหลังจากบันทึกข้อมูล! ---
        current_balance = self.calculate_balance()
        notify_income(amount=float(amount), balance=current_balance)
        
        # รีเฟรชหน้าจอ (เหมือนเดิม)
        self.create_main_app_view()

    def calculate_balance(self):
        """คำนวณยอดคงเหลือ"""
        total_expense = sum(t['amount'] for t in self.transactions)
        return self.income - total_expense

    def get_recent_transactions(self, count=5):
        """ดึงรายการล่าสุด"""
        return self.transactions[-count:]

    def load_page(self, page_name):
        """เมธอดสำหรับโหลดหน้าต่างๆ ใน Content Frame"""
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
        """สร้าง View หลักที่มี Sidebar และ Content Frame"""
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