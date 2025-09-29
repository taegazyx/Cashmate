import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import bcrypt
import mysql.connector

# --- Database Settings ---
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "1234"
DB_NAME = "cashmath_db"

# ---------------- Database Functions ----------------
def connect_db():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {err}")
        return None

def check_login(email, password):
    db = connect_db()
    if not db: return False
    try:
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
        result = cursor.fetchone()
        if result:
            hashed_password_from_db = result[0].encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), hashed_password_from_db)
        return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Login Check Error: {err}")
        return False
    finally:
        if db.is_connected():
            db.close()

def register_user(email, password):
    db = connect_db()
    if not db: return
    try:
        cursor = db.cursor()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password.decode("utf-8")))
        db.commit()
        messagebox.showinfo("Success", "ลงทะเบียนสำเร็จ!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not register user: {err}")
        db.rollback()
    finally:
        if db.is_connected():
            db.close()

# ---------------- Main App ----------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("790x480")
        self.resizable(0, 0)
        self.title("CASHMATH")

        self.login_frame = ctk.CTkFrame(master=self, fg_color="#ffffff")
        self.dashboard_frame = ctk.CTkFrame(master=self, fg_color="#F8F8FF")

        self.create_login_widgets()
        self.login_frame.pack(fill="both", expand=True)

    # ---------------- Login Actions ----------------
    def login_action(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not email or not password:
            messagebox.showwarning("Input Error", "กรุณากรอกอีเมลและรหัสผ่าน")
            return
        if check_login(email, password):
            messagebox.showinfo("Login Success", f"ยินดีต้อนรับ {email}")
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    def register_action(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        if not email or not password or not confirm_password:
            messagebox.showwarning("Input Error", "กรุณากรอกอีเมลและรหัสผ่านให้ครบถ้วน")
            return
        if password != confirm_password:
            messagebox.showerror("Password Error", "รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน")
            return
        register_user(email, password)

    # ---------------- Dashboard ----------------
    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)

        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        # Sidebar
        sidebar = ctk.CTkFrame(self.dashboard_frame, width=200, fg_color="#601E88")
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="☰ Menu", font=("Arial Bold", 18), text_color="white").pack(pady=20)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="#F8F8FF")
        self.content_frame.pack(side="left", fill="both", expand=True)

        def load_content(content_name):
            for w in self.content_frame.winfo_children():
                w.destroy()
            ctk.CTkLabel(self.content_frame, text=content_name, font=("Arial Bold", 22),
                         text_color="#333333").pack(pady=30)
            # ฟังก์ชันทดสอบ
            if content_name == "Add Income/Expense":
                self.add_income_expense_ui()
            elif content_name == "History":
                self.show_history_ui()
            elif content_name == "Summary/Stats":
                self.show_summary_ui()
            elif content_name == "Budget":
                self.set_budget_ui()

        # Sidebar Buttons
        menu_items = [
            ("🏠 Dashboard", "Dashboard Home"),
            ("➕ Add Income/Expense", "Add Income/Expense"),
            ("📜 History", "History"),
            ("📊 Summary/Stats", "Summary/Stats"),
            ("💰 Budget", "Budget"),
        ]
        for text, page in menu_items:
            ctk.CTkButton(sidebar, text=text, fg_color="#7733AA", hover_color="#9955CC",
                          command=lambda p=page: load_content(p)).pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(sidebar, text="🚪 Logout", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.logout).pack(fill="x", side="bottom", pady=20, padx=10)

        load_content("Welcome to Dashboard!")

    # ---------------- Dashboard UI Components ----------------
    def add_income_expense_ui(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="#EEEEEE", corner_radius=10)
        frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(frame, text="Add Income/Expense", font=("Arial Bold", 18)).pack(pady=10)
        ctk.CTkEntry(frame, placeholder_text="Description").pack(pady=5, padx=10, fill="x")
        ctk.CTkEntry(frame, placeholder_text="Amount").pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(frame, text="Add", command=lambda: messagebox.showinfo("Test", "Added!")).pack(pady=10)

    def show_history_ui(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="#EEEEEE", corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Transaction History (Test Data)", font=("Arial Bold", 18)).pack(pady=10)
        for i in range(5):
            ctk.CTkLabel(frame, text=f"{i+1}. Sample Transaction {i+1}").pack(anchor="w", padx=10)

    def show_summary_ui(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="#EEEEEE", corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        ctk.CTkLabel(frame, text="Summary & Statistics", font=("Arial Bold", 18)).pack(pady=10)
        ctk.CTkLabel(frame, text="Total Income: 10000").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text="Total Expense: 6000").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text="Balance: 4000").pack(anchor="w", padx=10)

    def set_budget_ui(self):
        frame = ctk.CTkFrame(self.content_frame, fg_color="#EEEEEE", corner_radius=10)
        frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(frame, text="Set Budget", font=("Arial Bold", 18)).pack(pady=10)
        ctk.CTkEntry(frame, placeholder_text="Monthly Budget").pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(frame, text="Save", command=lambda: messagebox.showinfo("Test", "Budget Saved!")).pack(pady=10)

    # ---------------- Logout ----------------
    def logout(self):
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    # ---------------- Login UI ----------------
    def create_login_widgets(self):
        right_frame = ctk.CTkFrame(master=self.login_frame, fg_color="#ffffff")
        right_frame.pack(expand=True, side="right", fill="both")

        center_frame = ctk.CTkFrame(master=right_frame, fg_color="#ffffff")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(master=center_frame, text="Welcome Back!", text_color="#601E88",
                     font=("Arial Bold", 24)).pack(pady=(0, 5))
        ctk.CTkLabel(master=center_frame, text="Sign in to your account", text_color="#7E7E7E",
                     font=("Arial", 12)).pack()

        ctk.CTkLabel(master=center_frame, text="✉️ Email:", text_color="#601E88", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=5)
        self.email_entry = ctk.CTkEntry(master=center_frame, width=250, fg_color="#EEEEEE",
                                        border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=5)

        ctk.CTkLabel(master=center_frame, text="🔒 Password:", text_color="#601E88", font=("Arial Bold", 14)).pack(anchor="w", pady=(20, 0), padx=5)
        self.password_entry = ctk.CTkEntry(master=center_frame, width=220, fg_color="#EEEEEE",
                                           border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(anchor="w", padx=5)

        def toggle_password():
            if self.password_entry.cget("show") == "":
                self.password_entry.configure(show="*")
            else:
                self.password_entry.configure(show="")
        ctk.CTkButton(master=center_frame, text="👁", width=25, command=toggle_password,
                       fg_color="#EEEEEE", hover_color="#DDDDDD", text_color="#601E88").pack(anchor="w", padx=5)

        ctk.CTkLabel(master=center_frame, text="🔒 Confirm Password:", text_color="#601E88", font=("Arial Bold", 14)).pack(anchor="w", pady=(10,0), padx=5)
        self.confirm_password_entry = ctk.CTkEntry(master=center_frame, width=250, fg_color="#EEEEEE",
                                                   border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.confirm_password_entry.pack(anchor="w", padx=5)

        button_frame = ctk.CTkFrame(master=center_frame, fg_color="transparent")
        button_frame.pack(pady=(30, 10), fill="x", padx=5)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(master=button_frame, text="Login", fg_color="#601E88",
                      hover_color="#E44982", font=("Arial Bold", 12),
                      text_color="#ffffff", command=self.login_action).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(master=button_frame, text="Register", fg_color="#EEEEEE",
                      hover_color="#DDDDDD", font=("Arial Bold", 12),
                      text_color="#601E88", command=self.register_action).grid(row=0, column=1, sticky="ew", padx=(5, 0))

if __name__ == "__main__":
    app = App()
    app.mainloop()
