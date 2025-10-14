# page_history.py
import tkinter as tk
import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk 
try:
    from tkcalendar import DateEntry
    has_calendar = True
except ImportError:
    has_calendar = False

# --- Mock Data and Constants (เก็บไว้นอกคลาสได้) ---
MOCK_BALANCE = 30664.25 
TRANSACTIONS = [
    {"date": "2025-10-14", "desc": "Freelance Payment", "amount": 5000.00, "type": "Income"},
    {"date": "2025-10-14", "desc": "Grocery Shopping", "amount": -1250.75, "type": "Expense"},
    {"date": "2025-10-14", "desc": "Rent Payment", "amount": -1250.75, "type": "Expense"},
]
DARK_GREEN = "#38761d"
BALANCE_CARD_GREEN = "#e5f5e5"
INCOME_GREEN = "#38761d"
EXPENSE_RED = "#cc0000"

# --- 1. สร้าง Class เพื่อห่อหุ้มโค้ดทั้งหมด ---
class HistoryPage:
    # --- 2. สร้าง __init__ ที่รับ parent (content_frame จากไฟล์หลัก) ---
    def __init__(self, parent):
        # สร้าง Frame หลักของหน้านี้ ให้เต็มพื้นที่ของ parent
        self.main_container = ctk.CTkFrame(parent, fg_color="#e8ffe8")
        self.main_container.pack(fill="both", expand=True)
        
        # --- 3. ย้ายโค้ด UI เดิมทั้งหมดมาไว้ตรงนี้ ---
        #    และเปลี่ยน parent เดิม (เช่น root) ให้เป็น self.main_container
        
        # Back Button (อาจจะไม่ต้องใช้แล้ว เพราะไฟล์หลักมี Sidebar อยู่แล้ว)
        # arrow_btn = ArrowButton(self.main_container, command=self.back_action)
        # arrow_btn.place(x=16, y=16)

        # Header and Bank Icon
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.place(relx=0.5, y=50, anchor="center") # ปรับตำแหน่ง Y เล็กน้อย
        # ... (โค้ดรูปภาพ bank.png เหมือนเดิม) ...

        ctk.CTkLabel(header_frame, text="CashMate App", 
                     font=ctk.CTkFont(size=14, weight="bold"), 
                     text_color=DARK_GREEN).pack()
        
        # HISTORY Title
        ctk.CTkLabel(self.main_container, text="HISTORY", 
                     font=ctk.CTkFont(size=50, weight="bold"), 
                     text_color=DARK_GREEN).place(relx=0.5, y=120, anchor="center")

        # Balance Display Card
        balance_frame = ctk.CTkFrame(self.main_container, fg_color=BALANCE_CARD_GREEN, corner_radius=10, 
                                     height=90, border_width=1, border_color=DARK_GREEN) 
        balance_frame.pack_propagate(False)
        balance_frame.place(relx=0.5, y=220, anchor="center", relwidth=0.9) 

        ctk.CTkLabel(balance_frame, text="Current Balance",
                     font=ctk.CTkFont(size=14), text_color="black").pack(pady=(5, 0)) 
        ctk.CTkLabel(balance_frame, text=f"{MOCK_BALANCE:,.2f} THB",
                     font=ctk.CTkFont(family="Inter", size=30, weight="bold"),
                     text_color=DARK_GREEN).pack()

        # Transaction List Header with Date Picker
        header_tx_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_tx_frame.place(relx=0.5, y=300, anchor="center", relwidth=0.9)
        # ... (โค้ดส่วน Header ของ Transaction เหมือนเดิม) ...
        ctk.CTkLabel(header_tx_frame, text="Recent Transactions", font=ctk.CTkFont(size=14, weight="bold"), text_color="black").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header_tx_frame, text="DATE:", font=ctk.CTkFont(size=14, weight="bold"), text_color=DARK_GREEN).grid(row=0, column=1, sticky="e", padx=(0,2))
        
        # ทำให้ date_entry เป็นของคลาสนี้โดยใช้ self.
        if has_calendar:
            self.date_entry = DateEntry(header_tx_frame, width=12, background='#e5f5e5', foreground='black', borderwidth=1, date_pattern='yyyy-mm-dd')
            self.date_entry.set_date(datetime.date.today())
            self.date_entry.grid(row=0, column=2, sticky="e")
            self.date_entry.bind("<<DateEntrySelected>>", self.on_date_change)
        else:
            self.date_entry = ctk.CTkEntry(header_tx_frame, width=100)
            self.date_entry.grid(row=0, column=2, sticky="e")
            self.date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
            self.date_entry.bind("<Return>", self.on_date_change)


        # Transaction Items Container
        self.tx_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.tx_container.place(relx=0.5, y=325, anchor="n", relwidth=0.9)

        # Initial display
        self.on_date_change()


    # --- 4. เปลี่ยนฟังก์ชันเดิม ให้เป็นเมธอดของคลาส (เพิ่ม self) ---
    def create_transaction_item(self, parent_frame, transaction):
        amount = transaction['amount']
        amount_text = f"{amount:+,.2f}"
        color = INCOME_GREEN if amount > 0 else EXPENSE_RED
        item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
        item_frame.pack(fill="x", pady=7)
        item_frame.grid_columnconfigure(1, weight=1)
        color_strip = ctk.CTkFrame(item_frame, fg_color=color, width=5, height=45, corner_radius=3)
        color_strip.grid(row=0, column=0, sticky="nsw", padx=(0, 10), rowspan=2)
        ctk.CTkLabel(item_frame, text=transaction['desc'], font=ctk.CTkFont(size=15), text_color="black", anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(item_frame, text=transaction['date'], font=ctk.CTkFont(size=12), text_color="#555555", anchor="w").grid(row=1, column=1, sticky="w")
        ctk.CTkLabel(item_frame, text=amount_text, font=ctk.CTkFont(size=18, weight="bold"), text_color=color, anchor="e").grid(row=0, column=2, sticky="e", padx=5, rowspan=2)

    def update_transaction_list(self, selected_date):
        for widget in self.tx_container.winfo_children():
            widget.destroy()
        filtered = [tx for tx in TRANSACTIONS if tx['date'] == selected_date]
        for tx in filtered:
            self.create_transaction_item(self.tx_container, tx)

    def on_date_change(self, event=None):
        if has_calendar:
            date = self.date_entry.get_date().strftime("%Y-%m-%d")
        else:
            date = self.date_entry.get()
        self.update_transaction_list(date)
        
    def back_action(self):
        messagebox.showinfo("Navigation", "This should return to the main dashboard.")