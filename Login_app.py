import customtkinter as ctk
from PIL import Image
import mysql.connector
from tkinter import messagebox
import bcrypt

# --- ส่วนของการตั้งค่าฐานข้อมูล ---
# (กรุณาเปลี่ยนค่าเหล่านี้ให้ตรงกับการตั้งค่า MariaDB ของคุณ)
DB_HOST = "127.0.0.1"  # หรือ "localhost"
DB_USER = "root"
DB_PASSWORD = "1234"   # ใส่รหัสผ่านที่ถูกต้อง
DB_NAME = "cashmath_db"

# ถ้าหากลองใช้รหัสผ่านเป็นค่าว่างแล้วยังไม่ได้ 
# ให้ใส่รหัสผ่าน MariaDB ที่ถูกต้องของคุณลงในเครื่องหมาย "" นี้
# เช่น DB_PASSWORD = "1234"

# ---------------- Database Functions ----------------
def connect_db():
    """สร้างและคืนค่าการเชื่อมต่อกับฐานข้อมูล"""
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
    """ตรวจสอบข้อมูลการล็อกอินจากฐานข้อมูล"""
    db = connect_db()
    if not db: return False

    try:
        cursor = db.cursor()
        # 1. ดึงรหัสผ่านที่ถูกเข้ารหัส (hashed password) จาก DB ตามอีเมลที่ผู้ใช้กรอก
        sql_query = "SELECT password FROM users WHERE email=%s"
        cursor.execute(sql_query, (email,))
        result = cursor.fetchone() # ดึงข้อมูลมาแค่ 1 แถว

        if result:
            # 2. นำรหัสผ่านที่ถูกเข้ารหัสมาเปรียบเทียบกับรหัสที่ผู้ใช้กรอก
            hashed_password_from_db = result[0].encode("utf-8")
            user_password = password.encode("utf-8")
            # ใช้ bcrypt ตรวจสอบว่าตรงกันหรือไม่
            return bcrypt.checkpw(user_password, hashed_password_from_db)
        return False # ไม่พบอีเมลในระบบ
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Login Check Error: {err}")
        return False
    finally:
        if db.is_connected():
            db.close()

def check_email_exists(email):
    """ตรวจสอบว่ามีอีเมลนี้อยู่ในระบบแล้วหรือยัง"""
    db = connect_db()
    if not db: return True # ถ้าต่อ DB ไม่ได้ ให้ถือว่ามีปัญหาไว้ก่อน

    try:
        cursor = db.cursor()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        return True if result else False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Email Check Error: {err}")
        return True # ป้องกันการสมัครซ้ำซ้อนหากเกิดข้อผิดพลาด
    finally:
        if db.is_connected():
            db.close()

def register_user(email, password):
    """บันทึกข้อมูลผู้ใช้ใหม่ลงในฐานข้อมูล"""
    if check_email_exists(email):
        messagebox.showerror("Registration Failed", f"อีเมล '{email}' นี้มีผู้ใช้งานแล้ว")
        return

    db = connect_db()
    if not db: return

    try:
        cursor = db.cursor()
        # 1. เข้ารหัสรหัสผ่านที่ผู้ใช้กรอกด้วย bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # 2. บันทึกอีเมลและรหัสผ่านที่เข้ารหัสแล้วลงในฐานข้อมูล
        sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
        # ต้องแปลง hashed_password กลับเป็น string ก่อนบันทึก
        val = (email, hashed_password.decode("utf-8"))
        cursor.execute(sql, val)
        db.commit() # ยืนยันการเปลี่ยนแปลงข้อมูล
        messagebox.showinfo("Success", "ลงทะเบียนสำเร็จ!\nคุณสามารถเข้าสู่ระบบได้ทันที")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not register user: {err}")
        db.rollback() # ยกเลิกการเปลี่ยนแปลงหากเกิดข้อผิดพลาด
    finally:
        if db.is_connected():
            db.close()
    # ...existing code...

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

# ...existing code...

def create_login_widgets(self):
    # ...existing code...
    ctk.CTkLabel(master=center_frame, text="🔒 Password:", text_color="#601E88", font=("Arial Bold", 14),
                 compound="left").pack(anchor="w", pady=(20, 0), padx=5)

    password_frame = ctk.CTkFrame(master=center_frame, fg_color="transparent")
    password_frame.pack(anchor="w", padx=5)

    self.password_entry = ctk.CTkEntry(master=password_frame, width=220, fg_color="#EEEEEE",
                                    border_color="#601E88", border_width=1, text_color="#000000", show="*")
    self.password_entry.pack(side="left")

    def toggle_password():
        if self.password_entry.cget("show") == "":
            self.password_entry.configure(show="*")
        else:
            self.password_entry.configure(show="")

    eye_button = ctk.CTkButton(master=password_frame, text="👁", width=25, command=toggle_password,
                               fg_color="#EEEEEE", hover_color="#DDDDDD", text_color="#601E88")
    eye_button.pack(side="left", padx=(5,0))

    # เพิ่มช่องกรอกยืนยันรหัสผ่าน
    ctk.CTkLabel(master=center_frame, text="🔒 Confirm Password:", text_color="#601E88", font=("Arial Bold", 14),
                 compound="left").pack(anchor="w", pady=(10, 0), padx=5)
    self.confirm_password_entry = ctk.CTkEntry(master=center_frame, width=250, fg_color="#EEEEEE",
                                               border_color="#601E88", border_width=1, text_color="#000000", show="*")
    self.confirm_password_entry.pack(anchor="w", padx=5)

    # ...existing code...

# ---------------- App ----------------
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

    # --------- Actions ---------
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

        if not email or not password:
            messagebox.showwarning("Input Error", "กรุณากรอกอีเมลและรหัสผ่านเพื่อลงทะเบียน")
            return
        
        register_user(email, password)

    # --------- Dashboard Layout ---------
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

        def load_content(content_text):
            for w in self.content_frame.winfo_children():
                w.destroy()
            ctk.CTkLabel(self.content_frame, text=content_text, font=("Arial Bold", 22), text_color="#333333").pack(pady=50)

        ctk.CTkButton(sidebar, text="🏠 Dashboard", fg_color="#7733AA", hover_color="#9955CC",
                      command=lambda: load_content("Dashboard Content")).pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(sidebar, text="📊 Reports", fg_color="#7733AA", hover_color="#9955CC",
                      command=lambda: load_content("Reports Content")).pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(sidebar, text="⚙️ Settings", fg_color="#7733AA", hover_color="#9955CC",
                      command=lambda: load_content("Settings Content")).pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(sidebar, text="🚪 Logout", fg_color="#AA3333", hover_color="#CC4444",
                      command=self.logout).pack(fill="x", side="bottom", pady=20, padx=10)


        load_content("Welcome to Dashboard!")

    def logout(self):
        self.dashboard_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    # ---------------- UI Creation ----------------
    def create_login_widgets(self):
        # --- หมายเหตุ: โค้ดส่วนรูปภาพถูกคอมเมนต์ไว้ ---
        # หากต้องการใช้รูปภาพ ให้สร้างไฟล์ภาพแล้วเอา comment ออก
        try:
            side_img_data = Image.open("side-img.png")
            # email_icon_data = Image.open("email-icon.png")
            # password_icon_data = Image.open("password-icon.png")

            side_img = ctk.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 480))
            # email_icon = ctk.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
            # password_icon = ctk.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
            ctk.CTkLabel(master=self.login_frame, text="", image=side_img).pack(expand=True, side="left", fill="y")
        except FileNotFoundError:
             # หากไม่มีไฟล์รูปภาพ ก็ไม่ต้องแสดง และโปรแกรมจะทำงานต่อไปได้
            print("Warning: Image files not found. Skipping image loading.")
            pass


        right_frame = ctk.CTkFrame(master=self.login_frame, fg_color="#ffffff")
        right_frame.pack(expand=True, side="right", fill="both")

        center_frame = ctk.CTkFrame(master=right_frame, fg_color="#ffffff")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(master=center_frame, text="Welcome Back!", text_color="#601E88", font=("Arial Bold", 24)).pack(pady=(0, 5))
        ctk.CTkLabel(master=center_frame, text="Sign in to your account", text_color="#7E7E7E", font=("Arial", 12)).pack()

        # ใช้ Text แทน Icon ชั่วคราว
        ctk.CTkLabel(master=center_frame, text="✉️ Email:", text_color="#601E88", font=("Arial Bold", 14),
                     compound="left").pack(anchor="w", pady=(20, 0), padx=5)
        self.email_entry = ctk.CTkEntry(master=center_frame, width=250, fg_color="#EEEEEE",
                                     border_color="#601E88", border_width=1, text_color="#000000")
        self.email_entry.pack(anchor="w", padx=5)

        ctk.CTkLabel(master=center_frame, text="🔒 Password:", text_color="#601E88", font=("Arial Bold", 14),
                     compound="left").pack(anchor="w", pady=(20, 0), padx=5)

        password_frame = ctk.CTkFrame(master=center_frame, fg_color="transparent")
        password_frame.pack(anchor="w", padx=5)

        self.password_entry = ctk.CTkEntry(master=password_frame, width=220, fg_color="#EEEEEE",
                                        border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.password_entry.pack(side="left")

        def toggle_password():
            if self.password_entry.cget("show") == "":
                self.password_entry.configure(show="*")
            else:
                self.password_entry.configure(show="")

        eye_button = ctk.CTkButton(master=password_frame, text="👁", width=25, command=toggle_password,
                                   fg_color="#EEEEEE", hover_color="#DDDDDD", text_color="#601E88")
        eye_button.pack(side="left", padx=(5,0))

        button_frame = ctk.CTkFrame(master=center_frame, fg_color="transparent")
        button_frame.pack(pady=(30, 10), fill="x", padx=5)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        login_button = ctk.CTkButton(master=button_frame, text="Login", fg_color="#601E88",
                                     hover_color="#E44982", font=("Arial Bold", 12),
                                     text_color="#ffffff", command=self.login_action)
        login_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        register_button = ctk.CTkButton(master=button_frame, text="Register", fg_color="#EEEEEE",
                                        hover_color="#DDDDDD", font=("Arial Bold", 12),
                                        text_color="#601E88", command=self.register_action)
        register_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))


if __name__ == "__main__":
    app = App()
    app.mainloop()