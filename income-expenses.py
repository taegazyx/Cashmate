import customtkinter as ctk
import os
from PIL import Image, ImageTk

# ... (ส่วนการตั้งค่าเบื้องต้นและ class CashMateApp.__init__ เหมือนเดิม) ...

    def create_gradient_background(self):
        """โหลดและตั้งค่า bg.jpg เป็นพื้นหลังของหน้าต่างหลัก"""
        
        # 1. โหลดรูปภาพ bg.jpg
        bg_image_data = Image.open(os.path.join(IMAGE_PATH, "bg.jpg"))
        
        # 2. สร้าง CTkImage และปรับขนาดให้เต็มหน้าต่าง (400x700)
        # Note: การปรับขนาดนี้อาจทำให้ภาพยืด/หดเล็กน้อยเพื่อให้พอดี
        bg_image_data = bg_image_data.resize((400, 700), Image.LANCZOS)
        self.bg_image = ctk.CTkImage(bg_image_data, size=(400, 700))
        
        # 3. ใช้ CTkLabel วางรูปภาพ
        self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        
        # 4. ใช้ .place() เพื่อวางให้เต็มพื้นที่ (ซ้อนอยู่ด้านหลังองค์ประกอบอื่นๆ)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ... (เมธอดอื่นๆ ที่เหลือของ CashMateApp เหมือนเดิม) ...

# ตรวจสอบการมีอยู่ของไฟล์และรันแอปพลิเคชัน
if __name__ == "__main__":
    # ตรวจสอบว่าไฟล์ bg.jpg อยู่ในโฟลเดอร์เดียวกัน
    IMAGE_PATH = os.path.dirname(os.path.realpath(__file__))
    bg_file = os.path.join(IMAGE_PATH, "bg.jpg")

    if not os.path.exists(bg_file):
        print("⚠️ ข้อผิดพลาด: ไม่พบไฟล์ 'bg.jpg'")
        print("โปรดตรวจสอบว่าไฟล์ 'bg.jpg' อยู่ในโฟลเดอร์เดียวกันกับไฟล์ Python")
    else:
        app = CashMateApp()
        app.mainloop()