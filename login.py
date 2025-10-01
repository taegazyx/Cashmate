import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def login_action():
    #DB connect and verify username and password here
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password.")

root = tk.Tk()
root.title("CashMate App Login") # <----- App Name
root.geometry("400x700")# <----- App Size

icon_img = ImageTk.PhotoImage(file="bg.png") # <----- App Icon
root.iconphoto(False, icon_img)

canvas = tk.Canvas(root, width=400, height=700, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

bg_img = Image.open("BG2.png").resize((400, 700)) # <----- Background Image 
bg = ImageTk.PhotoImage(bg_img)
canvas.create_image(0, 0, image=bg, anchor="nw")

try:
    logo_img = Image.open("KMITL LOGO.png").resize((150, 150)) # <----- Logo Image
    logo = ImageTk.PhotoImage(logo_img)
    canvas.create_image(200, 100, image=logo)
except FileNotFoundError:
    canvas.create_text(200, 100, text="[Logo Missing]", fill="grey", font=("Arial", 14))

canvas.create_text(200, 200, text="CashMate App",       
                   font=("Arial", 24, "bold"), fill="#000000") # <----- App Name in Login Page




#UserName Entry and Label
canvas.create_text(80, 260, text="Username",        
                   font=("Arial", 12, "bold"),               # <----- User Name in Login Page
                   fill="#000000", anchor="w")                          

username_entry = tk.Entry(root, font=("Arial", 14), width=25,           # <----- User Name Box in Login Page
                          relief="flat", bg="#e0e0e0", fg="black",
                          insertbackground="black")
canvas.create_window(200, 285, window=username_entry)




#PassWord Entry and Label
canvas.create_text(80, 330, text="Password",
                   font=("Arial", 12, "bold"),           # <----- Password in Login Page
                   fill="#000000", anchor="w")

password_entry = tk.Entry(root, font=("Arial", 14), width=25, show="*",     # <----- Password Box in Login Page
                          relief="flat", bg="#e0e0e0", fg="black",
                          insertbackground="black")
canvas.create_window(200, 355, window=password_entry)



#Login Button
login_button = tk.Button(root, text="Log in", font=("Arial", 14, "bold"),
                         bg="#5ec57e", fg="white",
                         command=login_action,
                         relief="flat", activebackground="#4C704E", activeforeground="white")
canvas.create_window(200, 420, window=login_button)



username_entry.focus_set()
root.bind("<Return>", lambda e: login_button.invoke())

_pw_visible = {"v": False}
def _toggle_pw(event=None):
    _pw_visible["v"] = not _pw_visible["v"]
    password_entry.configure(show="" if _pw_visible["v"] else "*")

password_entry.bind("<Double-Button-1>", _toggle_pw)

root.mainloop()
