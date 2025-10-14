# page_dashboard.py
import customtkinter as ctk

class DashboardPage:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)

        # ตั้งค่า Grid Layout (2 แถว 2 คอลัมน์)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=2)

        # --- 1. Widget ยอดเงินคงเหลือ (บนซ้าย) ---
        balance_frame = ctk.CTkFrame(self.frame)
        balance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(balance_frame, text="Total Balance", font=("Arial", 16)).pack(pady=(10,0))
        ctk.CTkLabel(balance_frame, text="฿54,321.00", font=("Arial Bold", 36, "bold")).pack(expand=True)

        # --- 2. Widget สรุปรายรับ-รายจ่าย (กลางซ้าย) ---
        summary_frame = ctk.CTkFrame(self.frame)
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(summary_frame, text="Monthly Summary", font=("Arial", 16)).pack(pady=(10,0))
        # (ในอนาคตส่วนนี้สามารถเพิ่ม Progress Bar ได้)
        ctk.CTkLabel(summary_frame, text="Income: ฿25,000.00").pack(pady=5)
        ctk.CTkLabel(summary_frame, text="Expense: ฿12,500.00").pack(pady=5)


        # --- 3. Widget ปุ่มลัด (บนขวา) ---
        actions_frame = ctk.CTkFrame(self.frame)
        actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        actions_frame.grid_columnconfigure((0,1), weight=1)
        actions_frame.grid_rowconfigure(0, weight=1)
        # (ควรเชื่อม command ไปยังหน้า AddPage)
        ctk.CTkButton(actions_frame, text="➕ Add Income", height=50).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkButton(actions_frame, text="➖ Add Expense", height=50).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


        # --- 4. Widget รายการล่าสุด (กลางขวา) ---
        recent_frame = ctk.CTkFrame(self.frame)
        recent_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(recent_frame, text="Recent Transactions", font=("Arial", 16)).pack(pady=(10,0))
        # (ในอนาคตส่วนนี้จะดึงข้อมูลจริงมาแสดง)
        ctk.CTkLabel(recent_frame, text="- Starbucks  -฿120").pack(anchor="w", padx=10)
        ctk.CTkLabel(recent_frame, text="- 7-Eleven   -฿85").pack(anchor="w", padx=10)
        ctk.CTkLabel(recent_frame, text="+ Freelance  +฿5,000").pack(anchor="w", padx=10)