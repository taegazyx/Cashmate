# # ตัวอย่าง

# import mysql.connector
# from tkinter import messagebox

# # --- Database Config ---
# DB_HOST = "127.0.0.1"   # หรือ "localhost"
# DB_USER = "root"        # user ของคุณ
# DB_PASSWORD = "1234"    # ใส่รหัสผ่านจริงของคุณ
# DB_NAME = "cashmath_db" # ชื่อ database ที่คุณสร้างไว้

# def connect_db():
#     """สร้างและคืนค่าการเชื่อมต่อกับฐานข้อมูล"""
#     try:
#         return mysql.connector.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME
#         )
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Connection Error", f"ไม่สามารถเชื่อมต่อฐานข้อมูลได้: {err}")
#         return None
