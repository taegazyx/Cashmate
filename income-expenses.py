import customtkinter as ctk
from PIL import Image

# ---------- Global Variables ----------
income_amount = 0
balance_amount = 0

# ---------- กำหนดหมวดหมู่รายจ่าย ----------
categories = [
    {"name":"Food", "label":"อาหาร\nFood", "icon":"food.png"},
    {"name":"Transport", "label":"เดินทาง\nTransport", "icon":"transport.png"},
    {"name":"Entertainment", "label":"บันเทิง\nEntertainment", "icon":"entertainment.png"},
    {"name":"Other", "label":"อื่นๆ\nOther", "icon":"other.png"}
]

expenses = {cat["name"]:0 for cat in categories}

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
        expenses[category] += amount
        balance_label.configure(text=f"ยอดคงเหลือ (Total Balance) : {balance_amount} Bath")
        category_totals[category].configure(text=f"รวม: {expenses[category]} บาท")
    except (ValueError, TypeError):
        print("❌ ไม่ได้กรอกจำนวนเงินที่ถูกต้อง")

# ---------- UI Setup ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("CashMate App")
app.geometry("400x700")

# ---------- Background ----------
bg_image = ctk.CTkImage(light_image=Image.open("bg.jpg"), size=(400,700))
bg_label = ctk.CTkLabel(app, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ---------- Icons ----------
img_bank = ctk.CTkImage(light_image=Image.open("bank.png"), size=(60,60))
img_balance = ctk.CTkImage(light_image=Image.open("balance.png"), size=(40,40))
icon_images = {cat["name"]: ctk.CTkImage(light_image=Image.open(cat["icon"]), size=(70,70)) for cat in categories}

# ---------- Header + Income ----------
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(header_frame, image=img_bank, text="", fg_color="transparent").pack(pady=(0,5))
ctk.CTkLabel(header_frame, text="CashMate App", font=("Arial Rounded MT Bold",24),
             text_color="black", fg_color="transparent").pack(pady=(0,10))

income_frame = ctk.CTkFrame(header_frame, corner_radius=15, border_width=1, fg_color="white")
income_frame.pack(pady=5, fill="x")
income_entry = ctk.CTkEntry(income_frame, placeholder_text="กรอกจำนวนรายรับ (Bath)")
income_entry.pack(pady=10, padx=20)
income_btn = ctk.CTkButton(income_frame, text="บันทึกรายรับ", command=set_income)
income_btn.pack(pady=5)
income_label = ctk.CTkLabel(income_frame, text="รายรับ (Income) : xxxx Bath", font=("Arial",16))
income_label.pack(pady=10)

# ---------- Scrollable Expenses ----------
scroll_frame = ctk.CTkScrollableFrame(app, corner_radius=15, fg_color="transparent")
scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
scroll_frame.grid_columnconfigure((0,1), weight=1)

category_totals = {}

for idx, cat in enumerate(categories):
    row = idx // 2
    col = idx % 2
    btn = ctk.CTkButton(scroll_frame, text=cat["label"], image=icon_images[cat["name"]],
                        font=("Arial",14), height=100, width=120, compound="top",
                        command=lambda c=cat["name"]: add_expense(c),
                        fg_color="transparent", hover_color="lightgreen", text_color="black")
    btn.grid(row=row*2, column=col, padx=10, pady=(10,0), sticky="nsew")

    lbl = ctk.CTkLabel(scroll_frame, text="รวม: 0 บาท", font=("Arial",12),
                       fg_color="transparent", text_color="black")
    lbl.grid(row=row*2+1, column=col, pady=(5,15))
    category_totals[cat["name"]] = lbl

# ---------- Balance + Home Button ----------
bottom_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="transparent")
bottom_frame.pack(side="bottom", pady=10, padx=20, fill="x")

balance_frame = ctk.CTkFrame(bottom_frame, corner_radius=15, border_width=1, fg_color="white")
balance_frame.pack(pady=5, fill="x")
ctk.CTkLabel(balance_frame, image=img_balance, text="").pack(side="left", padx=10)
balance_label = ctk.CTkLabel(balance_frame, text="ยอดคงเหลือ (Total Balance) : xxxx Bath", font=("Arial",16))
balance_label.pack(pady=15)

home_btn = ctk.CTkButton(bottom_frame, text="Back to Home", font=("Arial Rounded MT Bold",16),
                         fg_color="green", text_color="white", hover_color="#006400",
                         width=200, height=40)
home_btn.pack(pady=5)

# ---------- Run ----------
app.mainloop()
