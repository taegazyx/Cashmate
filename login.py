import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import init_db, verify_user, create_user
import home


# -------------------- ACTIONS --------------------
def login_action():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    ok, msg = verify_user(username, password)
    if ok:
        home.open_home(root, username)
    else:
        messagebox.showerror("Login Failed", msg)


def register_action():
    fullname = reg_fullname_entry.get()
    username = reg_username_entry.get()
    password = reg_password_entry.get()
    confirm = reg_confirm_entry.get()

    if not (fullname and username and password and confirm):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    if password != confirm:
        messagebox.showwarning("Input Error", "Passwords do not match.")
        return

    ok, msg = create_user(fullname, username, password)
    if ok:
        messagebox.showinfo("Registration", msg)
        draw_login()
    else:
        messagebox.showerror("Registration Failed", msg)


# -------------------- PAGE SWITCH / HELPERS --------------------
current_widgets = []  # เก็บ widget ที่สร้างไว้

def clear_page():
    """ล้างหน้าและวาดพื้นหลังใหม่"""
    global current_widgets
    for w in current_widgets:
        try:
            w.destroy()
        except Exception:
            pass
    current_widgets = []
    canvas.delete("all")
    canvas.create_image(0, 0, image=bg, anchor="nw")


def attach_pw_toggle(entry_widget):
    """ดับเบิลคลิกเพื่อสลับโชว์/ซ่อนรหัส"""
    state = {"hide": True}
    def _toggle(_=None):
        state["hide"] = not state["hide"]
        entry_widget.configure(show="" if state["hide"] else "*")
    entry_widget.bind("<Double-Button-1>", _toggle)


# -------------------- LOGIN PAGE --------------------
def draw_login():
    clear_page()

    if logo is not None:
        canvas.create_image(x_center, y_start, image=logo)
    else:
        canvas.create_text(x_center, y_start, text="[Logo Missing]", fill="grey", font=("Arial", 14))

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

    # ลิงก์ไป Register
    link_to_reg = tk.Button(root, text="Create an account", font=("Arial", 11, "underline"),
                            fg="#0d6efd", bg="#ffffff", bd=0, cursor="hand2",
                            activeforeground="#0d6efd", command=draw_register)
    current_widgets.append(link_to_reg)
    canvas.create_window(x_center, y_start + 370, window=link_to_reg)

    username_entry.focus_set()
    root.bind("<Return>", lambda e: login_button.invoke())


# -------------------- REGISTER PAGE --------------------
def draw_register():
    clear_page()

    if logo is not None:
        canvas.create_image(x_center, y_start, image=logo)
    else:
        canvas.create_text(x_center, y_start, text="[Logo Missing]", fill="grey", font=("Arial", 14))

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

    # ลิงก์กลับ Login
    link_to_login = tk.Button(root, text="Back to Login", font=("Arial", 11, "underline"),
                              fg="#0d6efd", bg="#ffffff", bd=0, cursor="hand2",
                              activeforeground="#0d6efd", command=draw_login)
    current_widgets.append(link_to_login)
    canvas.create_window(x_center, y_start + 500, window=link_to_login)

    reg_fullname_entry.focus_set()
    root.bind("<Return>", lambda e: reg_button.invoke())


# -------------------- WINDOW / CANVAS / ASSETS --------------------
root = tk.Tk()
root.title("CashMate App Login")
root.geometry("900x600")

# ไอคอน
try:
    icon_img = tk.PhotoImage(file="bg.png")
    root.iconphoto(False, icon_img)
except Exception:
    pass

canvas = tk.Canvas(root, width=900, height=600, highlightthickness=0, bd=0, bg="#ffffff")
canvas.pack(fill="both", expand=True)

bg_img = Image.open("BG2.png").resize((900, 600))
bg = ImageTk.PhotoImage(bg_img)

try:
    logo_img_pil = Image.open("KMITL LOGO.png").resize((140, 140))
    logo = ImageTk.PhotoImage(logo_img_pil)
except Exception:
    logo = None

x_center = 300
y_start = 150

init_db()
draw_login()
root.mainloop()
