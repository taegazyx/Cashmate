import customtkinter as ctk
# Import the database execution function we created
from db_connector import execute_query

# Note: You must ensure a table named 'users' exists in your MariaDB 
# for the default SELECT query to work (e.g., CREATE TABLE users (id INT, name VARCHAR(100));)

class CashMateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # การตั้งค่าหน้าต่างหลัก (The main window settings)
        self.title("CashMate - การจัดการฐานข้อมูล")
        self.geometry("450x350")
        
        # สร้างส่วนประกอบต่างๆ (Create components)
        self.label = ctk.CTkLabel(self, 
                                  text="สถานะ MariaDB: รอการตรวจสอบ",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(pady=(30, 10))

        self.button = ctk.CTkButton(self, 
                                    text="ดึงข้อมูลผู้ใช้จาก CashMate DB", 
                                    command=self.fetch_data,
                                    fg_color="#00C853", hover_color="#00A040") # Green theme
        self.button.pack(pady=10)

        self.data_display = ctk.CTkTextbox(self, 
                                           width=400, 
                                           height=150,
                                           corner_radius=8)
        self.data_display.pack(pady=20, padx=20)

    def fetch_data(self):
        """Function to fetch data from MariaDB and display it in the GUI."""
        self.data_display.delete("1.0", "end")
        self.label.configure(text="สถานะ MariaDB: กำลังดึงข้อมูล...")
        
        try:
            # ใช้ฟังก์ชัน execute_query สำหรับ SELECT
            # Example query: Select 5 records from a 'users' table
            query = "SELECT user_id, name FROM users LIMIT 5" 
            results = execute_query(query)

            if results is not None:
                if len(results) > 0:
                    self.label.configure(text=f"✅ สถานะ MariaDB: สำเร็จ! ดึงข้อมูลมา {len(results)} แถว", text_color="#00C853")
                    self.data_display.insert("end", "--- ข้อมูลผู้ใช้ 5 รายล่าสุด ---\n\n")
                    
                    # แสดงผลข้อมูลใน Textbox
                    for row in results:
                        self.data_display.insert("end", f"ID: {row[0]}, Name: {row[1]}\n")
                else:
                     self.label.configure(text="⚠️ สถานะ MariaDB: สำเร็จ! แต่ไม่พบข้อมูลในตาราง users", text_color="#FFD700")
                     self.data_display.insert("end", "ไม่พบข้อมูลในตารางที่กำหนด (โปรดตรวจสอบตาราง 'users')")
            else:
                # This handles connection errors caught in db_connector
                self.label.configure(text="❌ สถานะ MariaDB: ล้มเหลว! (ตรวจสอบ Console)", text_color="#FF4444")
                self.data_display.insert("end", "ไม่สามารถเชื่อมต่อ/ดึงข้อมูลได้ โปรดตรวจสอบการตั้งค่าใน db_connector.py และสถานะ MariaDB Server")

        except Exception as e:
            # Catch unexpected errors (e.g., float conversion issues, import errors)
            self.label.configure(text="❌ เกิดข้อผิดพลาดที่ไม่คาดคิด", text_color="#FF4444")
            print(f"Unexpected error in CashMateApp: {e}")

if __name__ == "__main__":
    app = CashMateApp()
    app.mainloop()