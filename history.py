import tkinter as tk
import datetime
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk 
import mysql.connector 
import sys

try:
    from tkcalendar import DateEntry
    has_calendar = True
except ImportError:
    has_calendar = False
    print("Warning: tkcalendar not found. Using CTkEntry for date input.")


# Set CustomTkinter appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green") 

# --- Database Configuration (กำหนดค่าการเชื่อมต่อ MariaDB) ---
DB_CONFIG = {
    'host': '127.0.0.1',      # อัปเดตตามข้อมูลที่ระบุ
    'user': 'root',           # อัปเดตตามข้อมูลที่ระบุ
    'password': '25849',      # อัปเดตตามข้อมูลที่ระบุ
    'database': 'cashmate_db'  # อัปเดตตามข้อมูลที่ระบุ
}
MOCK_BALANCE = 0.00 
TODAY_DATE_STR = datetime.date.today().strftime("%Y-%m-%d")


# --- Database Management Functions ---

def get_db_connection():
    """สร้างและส่งคืนการเชื่อมต่อฐานข้อมูล MariaDB"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to MariaDB:\n{err}\n\nCheck DB_CONFIG and ensure the MariaDB service is running.")
        print(f"Failed to connect to MariaDB: {err}")
        sys.exit(1)


def setup_database_structure():
    """ตรวจสอบและสร้างตาราง 'transactions' หากยังไม่มี"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # สร้างตาราง Transactions
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                description VARCHAR(255) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                type VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        print("Table 'transactions' checked/created successfully.")
            
    except mysql.connector.Error as err:
        print(f"MariaDB error during table creation: {err}")
    finally:
        cursor.close()
        conn.close()


def get_cumulative_balance():
    """ดึงยอดรวม (SUM) ของคอลัมน์ amount จากทุกรายการในฐานข้อมูล"""
    balance = 0.00
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # SQL query เพื่อรวมยอดทั้งหมด
        sql_query = "SELECT SUM(amount) FROM transactions"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        
        if result and result[0] is not None:
            # แปลง Decimal/String จาก DB เป็น float
            balance = float(result[0])
            
    except mysql.connector.Error as err:
        print(f"Error calculating balance from MariaDB: {err}")
    finally:
        cursor.close()
        conn.close()
        
    return balance


def get_transactions_by_date(selected_date):
    """ดึงข้อมูลธุรกรรมจากฐานข้อมูล MariaDB ตามวันที่ที่เลือก"""
    transactions_list = []
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        sql_select = "SELECT date, description, amount, type FROM transactions WHERE date = %s ORDER BY id DESC"
        cursor.execute(sql_select, (selected_date,))
        rows = cursor.fetchall()
        
        for row in rows:
            transactions_list.append({
                "date": row[0].strftime("%Y-%m-%d"), 
                "desc": row[1],
                "amount": float(row[2]),            
                "type": row[3]
            })
            
    except mysql.connector.Error as err:
        print(f"Error fetching data from MariaDB: {err}")
    finally:
        cursor.close()
        conn.close()
            
    return transactions_list

# **เรียกใช้ฟังก์ชันเริ่มต้นของฐานข้อมูล**
setup_database_structure() 
# ----------------------------------------------------------------


def calculate_balance():
    """ดึงยอดคงเหลือทั้งหมดจากฐานข้อมูล"""
    return get_cumulative_balance()

def back_action():
    """Placeholder for the action when the back button is pressed."""
    messagebox.showinfo("Navigation", "Navigating back to the Home/Dashboard page.")


# --- UI Setup ---
root = ctk.CTk()
root.title("CashMate History - Connected to MariaDB")
root.geometry("900x600")
root.resizable(False, False)


# --- Colors matching the image theme ---
DARK_GREEN = "#38761d" 
BALANCE_CARD_GREEN = "#e5f5e5" 
INCOME_GREEN = "#38761d" 
EXPENSE_RED = "#cc0000"


# --- Background Image Setup ---
try:
    bg_img = Image.open("BG2.png").resize((900, 600))
    bg_photo_image = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(root._w, image=bg_photo_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    main_container = ctk.CTkFrame(root, fg_color="transparent")
except FileNotFoundError as e:
    main_container = ctk.CTkFrame(root, fg_color="#e8ffe8")
except Exception as e:
    main_container = ctk.CTkFrame(root, fg_color="#e8ffe8")

main_container.pack(fill="both", expand=True)


# 1. Back Button
class ArrowButton(ctk.CTkFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, width=48, height=48, fg_color="transparent", **kwargs)
        self.canvas = ctk.CTkCanvas(self, width=48, height=48, highlightthickness=0)
        self.shadow = self.canvas.create_oval(6, 8, 42, 44, fill="#b6e2c6", outline="")
        self.circle = self.canvas.create_oval(4, 4, 44, 44, fill=INCOME_GREEN, outline="#38761d", width=2)
        self.arrow = self.canvas.create_polygon(22, 15, 15, 24, 22, 33, 22, 28, 33, 28, 33, 20, 22, 20,
                                     fill="white", outline="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda e: command() if command else None)
        self.canvas.bind("<Enter>", lambda e: self.canvas.itemconfig(self.circle, fill="#2e6e1a"))
        self.canvas.bind("<Leave>", lambda e: self.canvas.itemconfig(self.circle, fill=INCOME_GREEN))

arrow_btn = ArrowButton(main_container, command=back_action)
arrow_btn.place(x=16, y=16)

# 2. Header and Bank Icon
header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
header_frame.place(relx=0.5, y=120, anchor="center")

try:
    bank_img = Image.open("bank.png").resize((48, 48))
    bank_photo = ImageTk.PhotoImage(bank_img)
    bank_label = ctk.CTkLabel(header_frame, text="", image=bank_photo, fg_color="transparent")
    bank_label.image = bank_photo 
    bank_label.pack(pady=(0, 2))
except Exception as e:
    pass

ctk.CTkLabel(header_frame, text="CashMate App", 
             font=ctk.CTkFont(size=14, weight="bold"), 
             text_color=DARK_GREEN, 
             fg_color="transparent").pack()
             
# 3. HISTORY Title
ctk.CTkLabel(main_container, text="HISTORY", 
             font=ctk.CTkFont(size=50, weight="bold"), 
             text_color=DARK_GREEN, 
             fg_color="transparent").place(relx=0.5, y=190, anchor="center")


# 4. Balance Display Card
BALANCE = calculate_balance() # ดึงยอดรวมทั้งหมดจาก DB

balance_frame = ctk.CTkFrame(main_container, fg_color=BALANCE_CARD_GREEN, corner_radius=10, 
                             height=90, border_width=1, border_color=DARK_GREEN) 
balance_frame.pack_propagate(False)
balance_frame.place(relx=0.5, y=290, anchor="center", relwidth=0.9) 

ctk.CTkLabel(balance_frame, text="Current Balance",
             font=ctk.CTkFont(size=14, weight="normal"), fg_color="transparent", 
             text_color="black").pack(pady=(5, 0)) 

ctk.CTkLabel(balance_frame, text=f"{BALANCE:,.2f} THB",
             font=ctk.CTkFont(family="Inter", size=30, weight="bold"),
             fg_color="transparent", text_color=DARK_GREEN).pack()


# 5. Transaction List Header with Date Picker
header_tx_frame = ctk.CTkFrame(main_container, fg_color="transparent")
header_tx_frame.place(relx=0.5, y=370, anchor="center", relwidth=0.9)
header_tx_frame.grid_columnconfigure(0, weight=1)
header_tx_frame.grid_columnconfigure(1, weight=0)
header_tx_frame.grid_columnconfigure(2, weight=0)

ctk.CTkLabel(header_tx_frame, text="Recent Transactions",
             font=ctk.CTkFont(size=14, weight="bold"), 
             text_color="black", fg_color="transparent").grid(row=0, column=0, sticky="w")

ctk.CTkLabel(header_tx_frame, text="DATE:", font=ctk.CTkFont(size=14, weight="bold"), text_color=DARK_GREEN, fg_color="transparent").grid(row=0, column=1, sticky="e", padx=(0,2))
if has_calendar:
    date_var = tk.StringVar()
    date_entry = DateEntry(header_tx_frame, width=12, background='#e5f5e5', foreground='black', borderwidth=1, date_pattern='yyyy-mm-dd', textvariable=date_var)
    date_entry.set_date(datetime.date.today())
    date_entry.grid(row=0, column=2, sticky="e")
else:
    date_entry = ctk.CTkEntry(header_tx_frame, width=100)
    date_entry.insert(0, TODAY_DATE_STR)
    date_entry.grid(row=0, column=2, sticky="e")

# 6. Transaction Items Container (with filter)
tx_container = ctk.CTkFrame(main_container, fg_color="transparent")
tx_container.place(relx=0.5, y=395, anchor="n", relwidth=0.9)

def create_transaction_item(parent_frame, transaction):
    amount = transaction['amount']
    amount_text = f"{amount:+,.2f}"
    color = INCOME_GREEN if amount > 0 else EXPENSE_RED
    
    item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent", height=50)
    item_frame.pack(fill="x", pady=7)
    item_frame.grid_columnconfigure(1, weight=1)
    item_frame.grid_columnconfigure(2, weight=0)
    
    color_strip = ctk.CTkFrame(item_frame, fg_color=color, width=5, height=45, corner_radius=3)
    color_strip.grid(row=0, column=0, sticky="nsw", padx=(0, 10), rowspan=2)
    
    desc_label = ctk.CTkLabel(item_frame, text=transaction['desc'],
                              font=ctk.CTkFont(family="Inter", size=15, weight="normal"),
                              fg_color="transparent", text_color="black", anchor="w", justify="left")
    desc_label.grid(row=0, column=1, sticky="w")
    
    date_label = ctk.CTkLabel(item_frame, text=transaction['date'],
                              font=ctk.CTkFont(family="Inter", size=12, weight="normal"),
                              fg_color="transparent", text_color="#555555", anchor="w", justify="left")
    date_label.grid(row=1, column=1, sticky="w")
    
    amount_label = ctk.CTkLabel(item_frame, text=amount_text,
                                font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
                                fg_color="transparent", text_color=color, anchor="e")
    amount_label.grid(row=0, column=2, sticky="e", padx=5, rowspan=2)

def update_transaction_list(selected_date):
    """ดึงข้อมูลธุรกรรมจากฐานข้อมูล MariaDB และแสดงผล"""
    for widget in tx_container.winfo_children():
        widget.destroy()
        
    filtered = get_transactions_by_date(selected_date)
    
    if not filtered:
         ctk.CTkLabel(tx_container, text=f"No transactions found for {selected_date}",
                   font=ctk.CTkFont(size=14), text_color="#777777").pack(pady=20)
    else:
        for tx in filtered:
            create_transaction_item(tx_container, tx)

def on_date_change(event=None):
    if has_calendar:
        date = date_entry.get_date().strftime("%Y-%m-%d")
    else:
        date = date_entry.get()
    update_transaction_list(date)

# Bind the date entry to the update function
if has_calendar:
    date_entry.bind("<<DateEntrySelected>>", on_date_change)
else:
    date_entry.bind("<Return>", on_date_change)

# Initial display (default date: today's date)
if has_calendar:
    initial_date = date_entry.get_date().strftime("%Y-%m-%d")
else:
    initial_date = date_entry.get()
    
update_transaction_list(initial_date)

root.mainloop()