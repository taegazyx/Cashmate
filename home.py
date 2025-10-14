# main_app.py
import customtkinter as ctk
from tkinter import messagebox
from page_history import HistoryPage


# ---------------- Main App ----------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.resizable(0, 0)
        self.title("CASHMATH")
        self.dashboard_frame = ctk.CTkFrame(master=self, fg_color="#F8F8FF")
        self.show_dashboard()

    def show_dashboard(self):
        self.dashboard_frame.pack(fill="both", expand=True)
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Sidebar
        sidebar = ctk.CTkFrame(self.dashboard_frame, width=200, fg_color="#601E88")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="☰ Menu", font=("Arial Bold", 18), text_color="white").pack(pady=20)

        # Content Frame (พื้นที่ว่างสำหรับแสดงผลหน้าต่างๆ)
        self.content_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#F8F8FF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # --- 3. แก้ไขฟังก์ชัน load_content ---
        def load_content(content_name):
            # ล้าง content_frame ทุกครั้งที่กดปุ่มใหม่
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # ตรวจสอบชื่อหน้า แล้วเรียกคลาสที่ถูกต้องมาแสดงผล
            if content_name == "Add Income/Expense":
                AddPage(parent=self.content_frame) # สร้าง object จากคลาส AddPage
            
            elif content_name == "History":
                HistoryPage(parent=self.content_frame) # สร้าง object จากคลาส HistoryPage
            
            elif content_name == "Summary/Stats":
                SummaryPage(parent=self.content_frame) # สร้าง object จากคลาส SummaryPage
            
            elif content_name == "Budget":
                BudgetPage(parent=self.content_frame) # สร้าง object จากคลาส BudgetPage
            
            else: # สำหรับหน้า Dashboard Home
                ctk.CTkLabel(self.content_frame, text=content_name, font=("Arial Bold", 22),
                             text_color="#333333").pack(pady=30)

        # Sidebar Buttons (เหมือนเดิม)
        menu_items = [
            ("🏠 Dashboard", "Dashboard Home"),
            ("➕ Add Income/Expense", "Add Income/Expense"),
            ("📜 History", "History"),
            ("📊 Summary/Stats", "Summary/Stats"),
            ("💰 Budget", "Budget"),
        ]
        for text, page in menu_items:
            ctk.CTkButton(sidebar, text=text, fg_color="#7733AA", hover_color="#9955CC",
                          command=lambda p=page: load_content(p)).pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(sidebar, text="🚪 Exit", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.quit_app).pack(fill="x", side="bottom", pady=20, padx=10)

        load_content("Welcome to Cashmate")

    # --- 2. ลบฟังก์ชัน UI เดิมทั้งหมดออก ---
    # เราไม่ต้องการ add_income_expense_ui(), show_history_ui() อีกต่อไป
    # เพราะย้ายไปไว้ในไฟล์ของแต่ละหน้าแล้ว

    def quit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()