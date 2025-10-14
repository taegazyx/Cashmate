# page_history.py (ฉบับแก้ไข)
import customtkinter as ctk

# --- ค่าสีต่างๆ สามารถเก็บไว้นอกคลาสได้ ---
DARK_GREEN = "#38761d"
BALANCE_CARD_GREEN = "#e5f5e5"
INCOME_COLOR = "#2ECC71" # สีเขียวสำหรับรายรับ
EXPENSE_COLOR = "#E74C3C" # สีแดงสำหรับรายจ่าย

class HistoryPage:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.frame = ctk.CTkFrame(parent, fg_color="#e8ffe8")
        self.frame.pack(fill="both", expand=True)

        # --- ดึงข้อมูลจริงจาก main_app ---
        balance = self.main_app.calculate_balance()
        all_transactions = self.main_app.transactions

        # --- สร้าง UI ทั้งหมดโดยใช้ข้อมูลจริง ---
        
        # Header (เหมือนเดิม)
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.place(relx=0.5, y=50, anchor="center")
        ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial", 14, "bold"), text_color=DARK_GREEN).pack()
        
        # Title
        ctk.CTkLabel(self.frame, text="HISTORY", font=("Arial", 50, "bold"), text_color=DARK_GREEN).place(relx=0.5, y=120, anchor="center")

        # Balance Display Card
        balance_frame = ctk.CTkFrame(self.frame, fg_color=BALANCE_CARD_GREEN, corner_radius=10, height=90, border_width=1, border_color=DARK_GREEN) 
        balance_frame.pack_propagate(False)
        balance_frame.place(relx=0.5, y=220, anchor="center", relwidth=0.9) 

        ctk.CTkLabel(balance_frame, text="Current Balance", font=("Arial", 14), text_color="black").pack(pady=(5, 0)) 
        # <--- แสดงผล Balance จริง
        ctk.CTkLabel(balance_frame, text=f"฿{balance:,.2f}", font=("Inter", 30, "bold"), text_color=DARK_GREEN).pack()

        # Scrollable Frame สำหรับแสดงรายการ
        scroll_frame = ctk.CTkScrollableFrame(self.frame, label_text="All Transactions")
        scroll_frame.place(relx=0.5, y=300, anchor="n", relwidth=0.9, relheight=0.45)

        # --- วนลูปเพื่อแสดงทุกรายการ ---
        if not all_transactions:
            ctk.CTkLabel(scroll_frame, text="No transactions recorded yet.").pack(expand=True)
        else:
            for tx in reversed(all_transactions): # reversed() เพื่อให้รายการล่าสุดอยู่บน
                self.create_transaction_item(scroll_frame, tx)

    def create_transaction_item(self, parent_frame, transaction):
        """สร้าง Widget สำหรับแสดง 1 รายการ Transaction"""
        
        # <--- ตรวจสอบประเภทและกำหนดรูปแบบการแสดงผล ---
        if transaction['type'] == 'Income':
            amount_str = f"+฿{transaction['amount']:,.2f}"
            color = INCOME_COLOR
            description = transaction.get('desc', 'Income')
        else: # 'Expense'
            amount_str = f"-฿{transaction['amount']:,.2f}"
            color = EXPENSE_COLOR
            description = f"{transaction.get('desc', 'N/A')} ({transaction.get('category', 'N/A')})"

        # สร้าง Frame สำหรับแต่ละรายการ
        item_frame = ctk.CTkFrame(parent_frame, fg_color="white")
        item_frame.pack(fill="x", pady=4, padx=4)

        desc_label = ctk.CTkLabel(item_frame, text=description, anchor="w", font=("Arial", 14))
        desc_label.pack(side="left", padx=10, pady=10)
        
        amount_label = ctk.CTkLabel(item_frame, text=amount_str, anchor="e", text_color=color, font=("Arial", 14, "bold"))
        amount_label.pack(side="right", padx=10, pady=10)