import customtkinter as ctk
from PIL import Image

# ---------- Global Variables ----------
income_amount = 0
balance_amount = 0

# ---------- Functions ----------
def set_income():
    global income_amount, balance_amount
    try:
        income_amount = int(income_entry.get())
        balance_amount = income_amount
        income_label.configure(text=f"รายรับ (Income) : {income_amount} Bath")
        balance_label.configure(text=f"ยอดคงเหลือ (Total Balance) : {balance_amount} Bath")
    except ValueError:
        income_label.configure(text="กรุณากรอกตัวเลข Income")

def add_expense(category):
    global balance_amount
    dialog = ctk.CTkInputDialog(text=f"กรอกจำนวนเงินที่จ่าย ({category})", title="เพิ่มรายจ่าย")
    amount_str = dialog.get_input()
    try:
        amount = int(amount_str)
        balance_amount -= amount
        balance_label.configure(text=f"ยอดคงเหลือ (Total Balance) : {balance_amount} Bath")
        print(f"- {category} {amount} Bath (เหลือ {balance_amount} Bath)")
    except (ValueError, TypeError):
        print("❌ ไม่ได้กรอกจำนวนเงินที่ถูกต้อง")