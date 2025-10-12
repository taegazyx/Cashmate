import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# -------------------- แอ็กชันพื้นฐาน --------------------
def login_action():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    # TODO: ตรวจ DB ที่นี่
    messagebox.showinfo("Login Successful", f"Welcome, {username}!")

def register_action():
    fullname = reg_fullname_entry.get()
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm  = reg_confirm_entry.get()

    if not (fullname and username and password and confirm):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    if password != confirm:
        messagebox.showwarning("Input Error", "Passwords do not match.")
        return
    # TODO: บันทึกผู้ใช้ใหม่ลง DB ที่นี่
    messagebox.showinfo("Registration", f"Account created for {username}!")
    draw_login()  # กลับไปหน้า Login หลังสมัครสำเร็จ

# -------------------- สลับหน้า/เลย์เอาต์ --------------------
current_widgets = []   # เก็บวิดเจ็ตที่ถูก create_window เพื่อทำลายตอนสลับหน้า
def clear_page():
    global current_widgets
    for w in current_widgets:
        try:
            w.destroy()
        except Exception:
            pass
    current_widgets = []
    canvas.delete("all")
    # วาดพื้นหลังทุกครั้ง
    canvas.create_image(0, 0, image=bg, anchor="nw")

def attach_pw_toggle(entry_widget):
    state = {"show": True}
    def _toggle(_=None):
        state["show"] = not state["show"]
        entry_widget.configure(show="" if state["show"] else "*")
    entry_widget.bind("<Double-Button-1>", _toggle)

# -------------------- หน้า LOGIN --------------------
def draw_login():
    clear_page()

    # โลโก้
    try:
        canvas.create_image(x_center, y_start, image=logo)
    except Exception:
        canvas.create_text(x_center, y_start, text="[Logo Missing]", fill="grey", font=("Arial", 14))

    # ชื่อแอป
    canvas.create_text(x_center, y_start + 100, text="CashMate App",
                       font=("Arial", 26, "bold"), fill="#000000")

    # Username
    canvas.create_text(x_center - 90, y_start + 170, text="Username",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    global username_entry
    username_entry = tk.Entry(root, font=("Arial", 14), width=25,
                              relief="flat", bg="#e0e0e0", fg="black",
                              insertbackground="black")
    current_widgets.append(username_entry)
    canvas.create_window(x_center, y_start + 200, window=username_entry)

    # Password
    canvas.create_text(x_center - 90, y_start + 240, text="Password",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    global password_entry
    password_entry = tk.Entry(root, font=("Arial", 14), width=25, show="*",
                              relief="flat", bg="#e0e0e0", fg="black",
                              insertbackground="black")
    attach_pw_toggle(password_entry)
    current_widgets.append(password_entry)
    canvas.create_window(x_center, y_start + 270, window=password_entry)

    # ปุ่ม Login
    login_button = tk.Button(root, text="Log in", font=("Arial", 14, "bold"),
                             bg="#5ec57e", fg="white",
                             command=login_action,
                             relief="flat", activebackground="#4C704E", activeforeground="white")
    current_widgets.append(login_button)
    canvas.create_window(x_center, y_start + 330, window=login_button)

    # ลิงก์ไปหน้า Register
    link_to_reg = tk.Button(root, text="Create an account", font=("Arial", 11, "underline"),
                            fg="#0d6efd", bg="#ffffff", bd=0, cursor="hand2",
                            activeforeground="#0d6efd", command=draw_register)
    current_widgets.append(link_to_reg)
    canvas.create_window(x_center, y_start + 370, window=link_to_reg)

    # โฟกัส + Enter = Login
    username_entry.focus_set()
    root.bind("<Return>", lambda e: login_button.invoke())

# -------------------- หน้า REGISTER --------------------
def draw_register():
    clear_page()

    # โลโก้
    try:
        canvas.create_image(x_center, y_start, image=logo)
    except Exception:
        canvas.create_text(x_center, y_start, text="[Logo Missing]", fill="grey", font=("Arial", 14))

    # ชื่อแอป (หัวข้อเปลี่ยน)
    canvas.create_text(x_center, y_start + 100, text="Create Account",
                       font=("Arial", 26, "bold"), fill="#000000")

    # Full name
    canvas.create_text(x_center - 90, y_start + 160, text="Full name",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    global reg_fullname_entry, reg_username_entry, reg_password_entry, reg_confirm_entry
    reg_fullname_entry = tk.Entry(root, font=("Arial", 14), width=25,
                                  relief="flat", bg="#e0e0e0", fg="black",
                                  insertbackground="black")
    current_widgets.append(reg_fullname_entry)
    canvas.create_window(x_center, y_start + 190, window=reg_fullname_entry)

    # Username
    canvas.create_text(x_center - 90, y_start + 230, text="Username",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    reg_username_entry = tk.Entry(root, font=("Arial", 14), width=25,
                                  relief="flat", bg="#e0e0e0", fg="black",
                                  insertbackground="black")
    current_widgets.append(reg_username_entry)
    canvas.create_window(x_center, y_start + 260, window=reg_username_entry)

    # Password
    canvas.create_text(x_center - 90, y_start + 300, text="Password",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    reg_password_entry = tk.Entry(root, font=("Arial", 14), width=25, show="*",
                                  relief="flat", bg="#e0e0e0", fg="black",
                                  insertbackground="black")
    attach_pw_toggle(reg_password_entry)
    current_widgets.append(reg_password_entry)
    canvas.create_window(x_center, y_start + 330, window=reg_password_entry)

    # Confirm Password
    canvas.create_text(x_center - 90, y_start + 370, text="Confirm password",
                       font=("Arial", 14, "bold"), fill="#000000", anchor="w")

    reg_confirm_entry = tk.Entry(root, font=("Arial", 14), width=25, show="*",
                                 relief="flat", bg="#e0e0e0", fg="black",
                                 insertbackground="black")
    attach_pw_toggle(reg_confirm_entry)
    current_widgets.append(reg_confirm_entry)
    canvas.create_window(x_center, y_start + 400, window=reg_confirm_entry)

    # ปุ่ม Register
    reg_button = tk.Button(root, text="Register", font=("Arial", 14, "bold"),
                           bg="#5ec57e", fg="white",
                           command=register_action,
                           relief="flat", activebackground="#4C704E", activeforeground="white")
    current_widgets.append(reg_button)
    canvas.create_window(x_center, y_start + 460, window=reg_button)

    # ลิงก์กลับหน้า Login
    link_to_login = tk.Button(root, text="Back to Login", font=("Arial", 11, "underline"),
                              fg="#0d6efd", bg="#ffffff", bd=0, cursor="hand2",
                              activeforeground="#0d6efd", command=draw_login)
    current_widgets.append(link_to_login)
    canvas.create_window(x_center, y_start + 500, window=link_to_login)

    reg_fullname_entry.focus_set()
    # Enter = Register
    root.bind("<Return>", lambda e: reg_button.invoke())

# -------------------- สร้างหน้าต่าง/รูปพื้นหลัง --------------------
root = tk.Tk()
root.title("CashMate App Login")
root.geometry("900x600")

# ไอคอน
icon_img = tk.PhotoImage(file="bg.png")
root.iconphoto(False, icon_img)

# Canvas และ BG
canvas = tk.Canvas(root, width=900, height=600, highlightthickness=0, bd=0, bg="#ffffff")
canvas.pack(fill="both", expand=True)

bg_img = Image.open("BG2.png").resize((900, 600))
bg = ImageTk.PhotoImage(bg_img)

# โลโก้
try:
    _logo_pil = Image.open("KMITL LOGO.png").resize((140, 140))
    logo = ImageTk.PhotoImage(_logo_pil)
except Exception:
    logo = None  # จะวาดเป็นข้อความแทน

# ตำแหน่งคอลัมน์ (เลย์เอาต์แนวตั้ง)
x_center = 300
y_start = 150

# เริ่มที่หน้า Login
draw_login()

root.mainloop()
