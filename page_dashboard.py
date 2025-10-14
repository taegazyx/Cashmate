# page_dashboard.py (ฉบับแก้ไข)
import customtkinter as ctk

class DashboardPage:
    # <--- แก้ไขบรรทัดนี้ให้รับ main_app ---
    def __init__(self, parent, main_app):
        self.main_app = main_app 
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=2)

        # --- ดึงข้อมูลจริงจาก main_app มาแสดง ---
        balance = self.main_app.calculate_balance()
        recent_transactions = self.main_app.get_recent_transactions()
        total_income = self.main_app.income
        total_expense = sum(t['amount'] for t in self.main_app.transactions)

        # --- Widget ยอดเงินคงเหลือ ---
        balance_frame = ctk.CTkFrame(self.frame)
        balance_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(balance_frame, text="Total Balance", font=("Arial", 16)).pack(pady=(10,0))
        ctk.CTkLabel(balance_frame, text=f"฿{balance:,.2f}", font=("Arial Bold", 36, "bold")).pack(expand=True)

        # --- Widget สรุปรายรับ-รายจ่าย ---
        summary_frame = ctk.CTkFrame(self.frame)
        summary_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(summary_frame, text="Monthly Summary", font=("Arial", 16)).pack(pady=(10,5))
        ctk.CTkLabel(summary_frame, text=f"Income: ฿{total_income:,.2f}", text_color="#2ECC71").pack(pady=5, padx=10, anchor="w")
        ctk.CTkLabel(summary_frame, text=f"Expense: ฿{total_expense:,.2f}", text_color="#E74C3C").pack(pady=5, padx=10, anchor="w")

        # --- Widget ปุ่มลัด ---
        actions_frame = ctk.CTkFrame(self.frame)
        actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_rowconfigure(0, weight=1)
        
        # เพิ่ม command ให้ปุ่มกดสลับหน้าได้
        add_income_btn = ctk.CTkButton(actions_frame, text="➕ Add Income/Expense", height=50,
                                       command=lambda: self.main_app.load_page("Add Income/Expense"))
        add_income_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- Widget รายการล่าสุด ---
        recent_frame = ctk.CTkFrame(self.frame)
        recent_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(recent_frame, text="Recent Transactions", font=("Arial", 16)).pack(pady=(10,5))

        if not recent_transactions:
            ctk.CTkLabel(recent_frame, text="No recent transactions.").pack(expand=True)
        else:
            for tx in reversed(recent_transactions):
                amount_str = f"-฿{tx['amount']:,.2f}"
                color = "#E74C3C"
                
                item_frame = ctk.CTkFrame(recent_frame, fg_color="transparent")
                item_frame.pack(fill="x", padx=20, pady=2)
                
                ctk.CTkLabel(item_frame, text=tx['desc'], anchor="w").pack(side="left")
                ctk.CTkLabel(item_frame, text=amount_str, anchor="e", text_color=color).pack(side="right")