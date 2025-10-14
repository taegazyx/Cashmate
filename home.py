# main_app.py
import customtkinter as ctk
from tkinter import messagebox
from page_history import HistoryPage
from page_profile import ProfilePage


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

        # Content Frame
        self.content_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#F8F8FF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        def load_content(content_name):
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # --- 3. แก้ไขเงื่อนไขการโหลดหน้า ---
            if content_name == "Add Income/Expense":
                # AddPage(parent=self.content_frame) # (ถ้ามีไฟล์นี้ ก็เปิดใช้งาน)
                pass # ลบ pass ออกเมื่อมี AddPage
            
            elif content_name == "History":
                HistoryPage(parent=self.content_frame)
            
            elif content_name == "Profile": # <--- เพิ่มเงื่อนไขสำหรับ Profile
                ProfilePage(parent=self.content_frame)

            # (ลบ elif ของ Summary และ Budget ออกไป)
            
            else: 
                ctk.CTkLabel(self.content_frame, text=content_name, font=("Arial Bold", 22),
                             text_color="#333333").pack(pady=30)

        # --- 2. แก้ไขรายการเมนูใน Sidebar ---
        menu_items = [
            ("🏠 Dashboard", "Dashboard Home"),
            ("➕ Add Income/Expense", "Add Income/Expense"),
            ("📜 History", "History"),
            ("👤 Profile", "Profile"), # <--- เพิ่ม Profile
            # ("📊 Summary/Stats", "Summary/Stats"), <--- ลบออก
            # ("💰 Budget", "Budget"), <--- ลบออก
        ]
        # ------------------------------------

        for text, page in menu_items:
            ctk.CTkButton(sidebar, text=text, fg_color="#7733AA", hover_color="#9955CC",
                          command=lambda p=page: load_content(p)).pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(sidebar, text="🚪 Exit", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.quit_app).pack(fill="x", side="bottom", pady=20, padx=10)

        load_content("Welcome to Cashmate")

    def quit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()