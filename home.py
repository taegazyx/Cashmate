# main_app.py (ฉบับเริ่มต้นที่ Dashboard)
import customtkinter as ctk
from tkinter import messagebox

# --- 1. Import ทุกหน้าที่จำเป็น (ยกเว้น Login) ---
from page_history import HistoryPage
from page_profile import ProfilePage
from page_dashboard import DashboardPage

# ---------------- Main App ----------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.resizable(0, 0)
        self.title("CASHMATH")

        # --- 2. เรียกใช้เมธอดสร้าง Dashboard ทันที ---
        self.create_dashboard_view()

    def create_dashboard_view(self):
        """
        เมธอดสำหรับสร้างหน้าหลักทั้งหมด (Dashboard + Sidebar)
        """
        # สร้าง Frame หลักสำหรับ Dashboard และ Sidebar
        dashboard_frame = ctk.CTkFrame(self, fg_color="#F8F8FF")
        dashboard_frame.pack(fill="both", expand=True)

        # --- Sidebar ---
        sidebar = ctk.CTkFrame(dashboard_frame, width=200, fg_color="#601E88")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="☰ Menu", font=("Arial Bold", 18), text_color="white").pack(pady=20)

        # --- Content Frame ---
        content_frame = ctk.CTkFrame(dashboard_frame, fg_color="#F8F8FF")
        content_frame.pack(side="left", fill="both", expand=True)

        def load_content(content_name):
            for widget in content_frame.winfo_children():
                widget.destroy()
            
            if content_name == "Dashboard Home":
                DashboardPage(parent=content_frame)
            elif content_name == "Add Income/Expense":
                AddPage(parent=content_frame)
            elif content_name == "History":
                HistoryPage(parent=content_frame)
            elif content_name == "Profile":
                ProfilePage(parent=content_frame)
            
        menu_items = [
            ("🏠 Dashboard", "Dashboard Home"),
            ("➕ Add Income/Expense", "Add Income/Expense"),
            ("📜 History", "History"),
            ("👤 Profile", "Profile"),
        ]

        for text, page in menu_items:
            ctk.CTkButton(sidebar, text=text, fg_color="#7733AA", hover_color="#9955CC",
                          command=lambda p=page: load_content(p)).pack(fill="x", pady=5, padx=10)
        
        # --- 3. เปลี่ยนปุ่ม Logout เป็น Exit ---
        ctk.CTkButton(sidebar, text="🚪 Exit", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.quit_app).pack(fill="x", side="bottom", pady=20, padx=10)

        # โหลดหน้า Dashboard เป็นหน้าแรก
        load_content("Dashboard Home")

    def quit_app(self):
        """ฟังก์ชันสำหรับปิดโปรแกรม"""
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()