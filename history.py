
import tkinter as tk
import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk 
import tkinter as tk
try:
    from tkcalendar import DateEntry
    has_calendar = True
except ImportError:
    has_calendar = False

# Set CustomTkinter appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green") 

# --- Mock Data ---
# กำหนดให้ยอดรวมเริ่มต้นตรงตามภาพตัวอย่าง: 30,664.25
MOCK_BALANCE = 30664.25 
TRANSACTIONS = [
    {"date": "2025-10-01", "desc": "Freelance Payment", "amount": 5000.00, "type": "Income"},
    {"date": "2025-10-01", "desc": "Grocery Shopping", "amount": -1250.75, "type": "Expense"},
    {"date": "2025-10-01", "desc": "Rent Payment", "amount": -1250.75, "type": "Expense"}, # ใช้ซ้ำเพื่อให้รายการมี 3 บรรทัดตามภาพ
]

def calculate_balance():
    """Returns the mock balance value from the image."""
    return MOCK_BALANCE

def back_action():
    """Placeholder for the action when the back button is pressed."""
    messagebox.showinfo("Navigation", "Navigating back to the Home/Dashboard page.")


# --- UI Setup ---
root = ctk.CTk()
root.title("CashMate History")
root.geometry("400x700")
root.resizable(False, False)


# --- Colors matching the image theme ---
DARK_GREEN = "#38761d"  # สีเขียวเข้มสำหรับข้อความหลักและ Title
BALANCE_CARD_GREEN = "#e5f5e5" # สีเขียวอ่อนมากสำหรับกรอบยอดคงเหลือ (Lightest Mint)
INCOME_GREEN = "#38761d" # ใช้สำหรับยอด +
EXPENSE_RED = "#cc0000"


# --- Colors matching the image theme ---
DARK_GREEN = "#38761d"  # สีเขียวเข้มสำหรับข้อความหลักและ Title
BALANCE_CARD_GREEN = "#e5f5e5" # สีเขียวอ่อนมากสำหรับกรอบยอดคงเหลือ (Lightest Mint)
INCOME_GREEN = "#38761d" # ใช้สำหรับยอด +
EXPENSE_RED = "#cc0000"

# --- Background Image Setup ---

try:
    bg_img = Image.open("BG2.png").resize((400, 700))
    bg_photo_image = ImageTk.PhotoImage(bg_img)
    # Use tk.Label for background (always bottom layer)
    bg_label = tk.Label(root._w, image=bg_photo_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    main_container = ctk.CTkFrame(root, fg_color="transparent")
except FileNotFoundError as e:
    print("Warning: BG2.png not found. Using solid background color: #e8ffe8.")
    main_container = ctk.CTkFrame(root, fg_color="#e8ffe8")
except Exception as e:
    print(f"Error loading image: {e}. Using solid background color.")
    main_container = ctk.CTkFrame(root, fg_color="#e8ffe8")

main_container.pack(fill="both", expand=True)


# 1. Back Button (Top Left - Modern Circular Arrow)

# Modern ArrowButton using CTkCanvas for compatibility
class ArrowButton(ctk.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, width=48, height=48, fg_color="transparent", **kwargs)
        self.canvas = ctk.CTkCanvas(self, width=48, height=48, highlightthickness=0)
        # Shadow
        self.shadow = self.canvas.create_oval(6, 8, 42, 44, fill="#b6e2c6", outline="")
        # Main circle
        self.circle = self.canvas.create_oval(4, 4, 44, 44, fill=INCOME_GREEN, outline="#38761d", width=2)
        # Arrow (white)
        self.arrow = self.canvas.create_polygon(22, 15, 15, 24, 22, 33, 22, 28, 33, 28, 33, 20, 22, 20,
                                  fill="white", outline="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda e: command() if command else None)
        # Hover effect for circle
        self.canvas.bind("<Enter>", lambda e: self.canvas.itemconfig(self.circle, fill="#2e6e1a"))
        self.canvas.bind("<Leave>", lambda e: self.canvas.itemconfig(self.circle, fill=INCOME_GREEN))

# Replace old button with new ArrowButton
arrow_btn = ArrowButton(main_container, command=back_action)
arrow_btn.place(x=16, y=16)

# 2. Header and Bank Icon (Approximate position in the image)
# จำลองไอคอนธนาคารและชื่อแอป
# ในภาพ: มีไอคอนอาคารธนาคารและคำว่า CashMate App อยู่ตรงกลางด้านบน
ctk.CTkLabel(main_container, text="CashMate App", 
             font=ctk.CTkFont(size=14, weight="bold"), 
             text_color=DARK_GREEN, 
             fg_color="transparent").place(relx=0.5, y=130, anchor="center") 
header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
header_frame.place(relx=0.5, y=120, anchor="center")

# bank.png image (centered)
try:
    bank_img = Image.open("bank.png").resize((48, 48))
    bank_photo = ImageTk.PhotoImage(bank_img)
    bank_label = ctk.CTkLabel(header_frame, text="", image=bank_photo, fg_color="transparent")
    bank_label.image = bank_photo  # keep reference
    bank_label.pack(pady=(0, 2))
except Exception as e:
    print(f"Warning: bank.png not found or error: {e}")

# App Title (centered below the icon)
ctk.CTkLabel(header_frame, text="CashMate App", 
             font=ctk.CTkFont(size=14, weight="bold"), 
             text_color=DARK_GREEN, 
             fg_color="transparent").pack()
# 3. HISTORY Title (Large, Bold, Green)
# ใช้ขนาด 50 และฟอนต์ที่ดูมีน้ำหนักมากขึ้น
ctk.CTkLabel(main_container, text="HISTORY", 
             font=ctk.CTkFont(size=50, weight="bold"), 
             text_color=DARK_GREEN, 
             fg_color="transparent").place(relx=0.5, y=190, anchor="center")


# 4. Balance Display Card
BALANCE = calculate_balance()

# กรอบยอดคงเหลือ: ใช้สีอ่อนตามภาพ
balance_frame = ctk.CTkFrame(main_container, fg_color=BALANCE_CARD_GREEN, corner_radius=10, 
                             height=90, border_width=1, border_color=DARK_GREEN) 
balance_frame.pack_propagate(False)
# ขยายความกว้างให้เกือบเต็ม
balance_frame.place(relx=0.5, y=290, anchor="center", relwidth=0.9) 

# Current Balance Text: สีดำบนพื้นหลังสีอ่อน
ctk.CTkLabel(balance_frame, text="Current Balance",
             font=ctk.CTkFont(size=14, weight="normal"), fg_color="transparent", 
             text_color="black").pack(pady=(5, 0)) 

# Balance Value: ใหญ่, หนา, สีเข้ม
ctk.CTkLabel(balance_frame, text=f"{BALANCE:,.2f} THB",
             font=ctk.CTkFont(family="Inter", size=30, weight="bold"),
             fg_color="transparent", text_color=DARK_GREEN).pack()



# 5. Transaction List Header with Date Picker
header_tx_frame = ctk.CTkFrame(main_container, fg_color="transparent")
header_tx_frame.place(relx=0.5, y=370, anchor="center", relwidth=0.9)
header_tx_frame.grid_columnconfigure(0, weight=1)
header_tx_frame.grid_columnconfigure(1, weight=0)

# Recent Transactions Text
ctk.CTkLabel(header_tx_frame, text="Recent Transactions",
             font=ctk.CTkFont(size=14, weight="bold"), 
             text_color="black", fg_color="transparent").grid(row=0, column=0, sticky="w")

# Date Picker (DateEntry if available, fallback to Entry)
ctk.CTkLabel(header_tx_frame, text="DATE:", font=ctk.CTkFont(size=14, weight="bold"), text_color=DARK_GREEN, fg_color="transparent").grid(row=0, column=1, sticky="e", padx=(0,2))
if has_calendar:
    date_var = tk.StringVar()
    date_entry = DateEntry(header_tx_frame, width=12, background='#e5f5e5', foreground='black', borderwidth=1, date_pattern='yyyy-mm-dd', textvariable=date_var)
    date_entry.set_date(datetime.date.today())
    date_entry.grid(row=0, column=2, sticky="e")
else:
    date_entry = ctk.CTkEntry(header_tx_frame, width=100)
    date_entry.grid(row=0, column=2, sticky="e")
    date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

# 6. Transaction Items Container (with filter)
tx_container = ctk.CTkFrame(main_container, fg_color="transparent")
tx_container.place(relx=0.5, y=395, anchor="n", relwidth=0.9)

def create_transaction_item(parent_frame, transaction):
    amount = transaction['amount']
    amount_text = f"{amount:+,.2f}"
    color = INCOME_GREEN if amount > 0 else EXPENSE_RED
    # Item Frame: โปร่งใส
    item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
    item_frame.pack(fill="x", pady=7)
    item_frame.grid_columnconfigure(1, weight=1)
    item_frame.grid_columnconfigure(2, weight=0)
    # Color Strip
    color_strip = ctk.CTkFrame(item_frame, fg_color=color, width=5, height=45, corner_radius=3)
    color_strip.grid(row=0, column=0, sticky="nsw", padx=(0, 10), rowspan=2)
    # Description
    desc_label = ctk.CTkLabel(item_frame, text=transaction['desc'],
                              font=ctk.CTkFont(family="Inter", size=15, weight="normal"),
                              fg_color="transparent", text_color="black", anchor="w", justify="left")
    desc_label.grid(row=0, column=1, sticky="w")
    # Date
    date_label = ctk.CTkLabel(item_frame, text=transaction['date'],
                              font=ctk.CTkFont(family="Inter", size=12, weight="normal"),
                              fg_color="transparent", text_color="#555555", anchor="w", justify="left")
    date_label.grid(row=1, column=1, sticky="w")
    # Amount
    amount_label = ctk.CTkLabel(item_frame, text=amount_text,
                                font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
                                fg_color="transparent", text_color=color, anchor="e")
    amount_label.grid(row=0, column=2, sticky="e", padx=5, rowspan=2)

def update_transaction_list(selected_date):
    # Clear all children in tx_container
    for widget in tx_container.winfo_children():
        widget.destroy()
    # Filter transactions by date
    filtered = [tx for tx in TRANSACTIONS if tx['date'] == selected_date]
    for tx in filtered:
        create_transaction_item(tx_container, tx)

def on_date_change(event=None):
    if has_calendar:
        date = date_entry.get_date().strftime("%Y-%m-%d")
    else:
        date = date_entry.get()
    update_transaction_list(date)

if has_calendar:
    date_entry.bind("<<DateEntrySelected>>", on_date_change)
else:
    date_entry.bind("<Return>", on_date_change)

# Initial display (default date)
if has_calendar:
    update_transaction_list(date_entry.get_date().strftime("%Y-%m-%d"))
else:
    update_transaction_list(date_entry.get())



# 6. Transaction Items Container (with filter)
tx_container = ctk.CTkFrame(main_container, fg_color="transparent")
tx_container.place(relx=0.5, y=395, anchor="n", relwidth=0.9)

def create_transaction_item(parent_frame, transaction):
    amount = transaction['amount']
    amount_text = f"{amount:+,.2f}"
    color = INCOME_GREEN if amount > 0 else EXPENSE_RED
    # Item Frame: โปร่งใส
    item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
    item_frame.pack(fill="x", pady=7)
    item_frame.grid_columnconfigure(1, weight=1)
    item_frame.grid_columnconfigure(2, weight=0)
    # Color Strip
    color_strip = ctk.CTkFrame(item_frame, fg_color=color, width=5, height=45, corner_radius=3)
    color_strip.grid(row=0, column=0, sticky="nsw", padx=(0, 10), rowspan=2)
    # Description
    desc_label = ctk.CTkLabel(item_frame, text=transaction['desc'],
                              font=ctk.CTkFont(family="Inter", size=15, weight="normal"),
                              fg_color="transparent", text_color="black", anchor="w", justify="left")
    desc_label.grid(row=0, column=1, sticky="w")
    # Date
    date_label = ctk.CTkLabel(item_frame, text=transaction['date'],
                              font=ctk.CTkFont(family="Inter", size=12, weight="normal"),
                              fg_color="transparent", text_color="#555555", anchor="w", justify="left")
    date_label.grid(row=1, column=1, sticky="w")
    # Amount
    amount_label = ctk.CTkLabel(item_frame, text=amount_text,
                                font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
                                fg_color="transparent", text_color=color, anchor="e")
    amount_label.grid(row=0, column=2, sticky="e", padx=5, rowspan=2)

def update_transaction_list(selected_date):
    # Clear all children in tx_container
    for widget in tx_container.winfo_children():
        widget.destroy()
    # Filter transactions by date
    filtered = [tx for tx in TRANSACTIONS if tx['date'] == selected_date]
    for tx in filtered:
        create_transaction_item(tx_container, tx)

# Initial display (default date)
update_transaction_list(date_entry.get())

root.mainloop()