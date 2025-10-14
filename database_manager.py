import mariadb
import sys
from CTkMessagebox import CTkMessagebox 

class DatabaseManager:
    """
    คลาสสำหรับจัดการการเชื่อมต่อและการดำเนินการกับฐานข้อมูล MariaDB
    """
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        """สร้างการเชื่อมต่อกับฐานข้อมูล"""
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database,
                port=3306 
            )
            print("เชื่อมต่อ MariaDB สำเร็จ!")
            self.create_table()
            return self.conn
        except mariadb.Error as e:
            error_msg = f"ไม่สามารถเชื่อมต่อ MariaDB ได้: {e}\n(โปรดตรวจสอบ DB Host/User/Pass)"
            CTkMessagebox(title="ข้อผิดพลาดการเชื่อมต่อ", message=error_msg, icon="cancel")
            sys.exit(1)
            
    def close(self):
        """ปิดการเชื่อมต่อฐานข้อมูล"""
        if self.conn:
            self.conn.close()
            print("ปิดการเชื่อมต่อ MariaDB แล้ว")
            
    # 🔴 เมธอดใหม่: ตรวจสอบและอัปเดตโครงสร้างตาราง
    def check_and_update_table_structure(self):
        """ตรวจสอบว่าคอลัมน์ category มีในตาราง transactions หรือไม่ และเพิ่มถ้ายังไม่มี"""
        try:
            cursor = self.conn.cursor()
            
            # คำสั่ง SQL เพื่อตรวจสอบคอลัมน์ (ใช้ DESCRIBE)
            cursor.execute("DESCRIBE transactions")
            columns = [col[0] for col in cursor.fetchall()]
            
            if 'category' not in columns:
                print("⚠️ ตรวจพบ: ตาราง transactions ขาดคอลัมน์ 'category' กำลังเพิ่มคอลัมน์...")
                # ใช้ ALTER TABLE เพื่อเพิ่มคอลัมน์ 'category'
                # กำหนดให้สามารถเป็น NULL ได้เพื่อไม่ให้กระทบกับรายการเก่าที่อาจมีอยู่
                cursor.execute("ALTER TABLE transactions ADD COLUMN category VARCHAR(50) NULL")
                self.conn.commit()
                print("✅ เพิ่มคอลัมน์ 'category' สำเร็จแล้ว")
                
            cursor.close()
        except mariadb.Error as e:
             # หากเกิดข้อผิดพลาดในการ DESCRIBE อาจเป็นเพราะตารางยังไม่มี
             # ซึ่งจะถูกจัดการในเมธอด create_table
             pass 

    def create_table(self):
        """สร้างตาราง transactions ถ้ายังไม่มี และตรวจสอบโครงสร้าง"""
        try:
            cursor = self.conn.cursor()
            # โค้ด CREATE TABLE ที่ถูกต้องและสมบูรณ์
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    type VARCHAR(10) NOT NULL, -- 'Income' หรือ 'Expense'
                    description VARCHAR(255) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    date DATE NOT NULL,
                    category VARCHAR(50) 
                )
            """)
            self.conn.commit()
            cursor.close()
            
            # 🔴 เรียกเมธอดตรวจสอบโครงสร้าง
            self.check_and_update_table_structure()

        except mariadb.Error as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title="ข้อผิดพลาด", message=f"เกิดข้อผิดพลาดในการสร้างตาราง: {e}", icon="warning")

    # ... (เมธอด add_transaction, fetch_total_by_type, fetch_category_totals โค้ดเดิม) ...
    # 💡 หมายเหตุ: เมธอดที่เหลือในไฟล์นี้ใช้โค้ดเดิมที่เคยรวมไว้ล่าสุดแล้ว

    def add_transaction(self, type, category, desc, amount, date):
        """เพิ่มรายการรายรับหรือรายจ่ายใหม่ลงในตาราง"""
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO transactions (type, category, description, amount, date) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (type, category, desc, amount, date))
            self.conn.commit()
            cursor.close()
            return True
        except mariadb.Error as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title="ข้อผิดพลาด", message=f"บันทึกรายการไม่สำเร็จ: {e}", icon="warning")
            return False

    def fetch_total_by_type(self, type_val):
        """ดึงยอดรวมของรายรับหรือรายจ่ายทั้งหมดจากตาราง transactions"""
        try:
            cursor = self.conn.cursor()
            query = "SELECT SUM(amount) FROM transactions WHERE type = ?"
            cursor.execute(query, (type_val,))
            
            total = cursor.fetchone()[0]
            cursor.close()
            
            return float(total) if total is not None else 0.00
            
        except mariadb.Error as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title="ข้อผิดพลาด", message=f"ดึงยอดรวมไม่สำเร็จ: {e}", icon="warning")
            return 0.00

    def fetch_category_totals(self):
        """ดึงยอดรวมรายจ่าย (Expense) แยกตามหมวดหมู่ทั้งหมด"""
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT category, SUM(amount) 
                FROM transactions 
                WHERE type = 'Expense'
                GROUP BY category
            """
            cursor.execute(query)
            
            category_totals = {row[0]: float(row[1]) for row in cursor.fetchall()}
            cursor.close()
            
            return category_totals
            
        except mariadb.Error as e:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title="ข้อผิดพลาด", message=f"ดึงยอดรวมหมวดหมู่ไม่สำเร็จ: {e}", icon="warning")
            return {}