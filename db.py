# db.py  (สำหรับ mysql-connector)
import mysql.connector as mysql
import bcrypt

DB_HOST = "127.0.0.1"
DB_PORT = 3307      # ถ้าคุณเปลี่ยนพอร์ตตอนติดตั้ง ให้ใส่เลขนั้น
DB_USER = "root"
DB_PASSWORD = "1234"  # ใส่ให้ตรงกับที่ตั้งตอนติดตั้ง
DB_NAME = "cashmate_db"

def connect_db():
    return mysql.connect(
        host=DB_HOST, port=DB_PORT,
        user=DB_USER, password=DB_PASSWORD,
        database=DB_NAME, autocommit=True
    )

def init_db():
    """สร้างตาราง users ถ้ายังไม่มี"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARBINARY(60) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARACTER SET utf8mb4
    """)
    cur.close(); conn.close()

def create_user(fullname: str, username: str, password: str) -> tuple[bool, str]:
    """สมัครผู้ใช้ใหม่"""
    try:
        conn = connect_db()
        cur = conn.cursor()

        # ใช้ %s สำหรับ mysql-connector
        cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return False, "Username นี้ถูกใช้แล้ว"

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cur.execute(
            "INSERT INTO users (fullname, username, password_hash) VALUES (%s, %s, %s)",
            (fullname, username, pw_hash)
        )
        return True, "สมัครสมาชิกสำเร็จ"
    except mysql.Error as e:
        return False, f"DB Error: {e}"
    finally:
        try:
            cur.close(); conn.close()
        except:
            pass

def verify_user(username: str, password: str) -> tuple[bool, str]:
    """ตรวจสอบเข้าสู่ระบบ"""
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if not row:
            return False, "ไม่พบบัญชีผู้ใช้"

        pw_hash = row[0]
        ok = bcrypt.checkpw(password.encode("utf-8"), pw_hash)
        return (True, "เข้าสู่ระบบสำเร็จ") if ok else (False, "รหัสผ่านไม่ถูกต้อง")
    except mysql.Error as e:
        return False, f"DB Error: {e}"
    finally:
        try:
            cur.close(); conn.close()
        except:
            pass
