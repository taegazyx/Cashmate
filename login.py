import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.title("CashMate App Login") # <----- App Name
root.geometry("400x700")# <----- App Size

canvas = tk.Canvas(root, width=400, height=700, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)


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
