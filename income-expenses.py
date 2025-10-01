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

# ---------- UI Setup ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("CashMate App")
app.geometry("400x700")

# ---------- ใส่ Background ----------
bg_image = ctk.CTkImage(light_image=Image.open("bg.jpg"), size=(400, 700))
bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)   # ทำให้เต็มหน้าต่าง

# ---------- โหลดไอคอน----------
img_bank = ctk.CTkImage(light_image=Image.open("bank.jpg"), size=(60, 60))
img_food = ctk.CTkImage(light_image=Image.open("food.jpg"), size=(60, 60))
img_transport = ctk.CTkImage(light_image=Image.open("transport.jpg"), size=(60, 60))
img_entertain = ctk.CTkImage(light_image=Image.open("entertainment.jpg"), size=(60, 60))
img_other = ctk.CTkImage(light_image=Image.open("other.jpg"), size=(60, 60))
img_balance = ctk.CTkImage(light_image=Image.open("balance.jpg"), size=(40, 40))

# ---------- ส่วนหัว -----------
title_frame = ctk.CTkFrame(app, fg_color="transparent")
title_frame.pack(pady=10)
ctk.CTkLabel(title_frame, image=img_bank, text="").pack()
ctk.CTkLabel(title_frame, text="CashMate App", font=("Arial Rounded MT Bold", 24)).pack()

# ---------- กรอก Income -----------
income_frame = ctk.CTkFrame(app, corner_radius=15, border_width=1)
income_frame.pack(pady=10, padx=20, fill="x")
income_entry = ctk.CTkEntry(income_frame, placeholder_text="กรอกจำนวนรายรับ (Bath)")
income_entry.pack(pady=10, padx=20)
income_btn = ctk.CTkButton(income_frame, text="บันทึกรายรับ", command=set_income)
income_btn.pack(pady=5)
income_label = ctk.CTkLabel(income_frame, text="รายรับ (Income) : xxxx Bath",
                            font=("Arial", 16))
income_label.pack(pady=10)