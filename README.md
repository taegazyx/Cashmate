# CASHMATH – ระบบ Login/Register + Dashboard

# โปรแกรมนี้เป็นแอปพลิเคชัน GUI สำหรับ ล็อกอิน / ลงทะเบียนผู้ใช้ โดยเชื่อมต่อกับฐานข้อมูล MySQL/MariaDB และใช้ bcrypt ในการเข้ารหัสรหัสผ่าน

# สร้างด้วย Python + CustomTkinter


# ฟีเจอร์

✅ ลงทะเบียนผู้ใช้ใหม่ (Register)

✅ ล็อกอินด้วยอีเมลและรหัสผ่าน

✅ เก็บรหัสผ่านแบบเข้ารหัส (bcrypt)

✅ แสดงหน้า Dashboard หลังเข้าสู่ระบบ

✅ UI สวยงามด้วย CustomTkinter

## ขั้นตอนติดตั้ง (สำหรับนักพัฒนา)
1. Python Libraries (ติดตั้งด้วย pip install)

   จากโค้ดนี้ต้องใช้ lib เหล่านี้:

  customtkinter → UI library แทน tkinter
  Pillow (PIL) → ใช้เปิด/จัดการรูปภาพ
  mysql-connector-python → ใช้เชื่อมต่อฐานข้อมูล MySQL/MariaDB
  bcrypt → ใช้เข้ารหัสรหัสผ่าน
  tkinter → มาพร้อมกับ Python อยู่แล้ว (ไม่ต้องติดตั้งเพิ่มถ้าใช้ Python มาตรฐาน)

2. Database (MariaDB/MySQL)

  ต้องติดตั้ง MariaDB หรือ MySQL ในเครื่องก่อน

  ต้องสร้างฐานข้อมูลชื่อ cashmath_db (ตามที่โค้ดกำหนด)

  ต้องสร้าง table users เช่น:

  CREATE DATABASE cashmath_db;

  USE cashmath_db; 

  CREATE TABLE users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      email VARCHAR(255) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL
  );

3. Environment

  Python 3.10 ขึ้นไป (แนะนำ)

  OS ที่รองรับ Tkinter (Windows, macOS, Linux)

  ถ้าใช้ macOS/Linux อาจต้องติดตั้ง python3-tk เพิ่ม

4. ไฟล์รูปภาพ (Optional)

  ถ้ามีไฟล์ side-img.png จะต้องวางไว้ในโฟลเดอร์เดียวกับไฟล์ .py

  ถ้าไม่มี โปรแกรมก็ยังรันได้ (โค้ดจัดการไว้แล้ว)

5. วิธีติดตั้ง Python และ Library

  pip install -r requirements.txt


# Clone repo:
  git clone https://github.com/taegazyx/Cashmate
  cd Cashmate

# สุดท้าย วิธีการใช้งาน

  รันโปรแกรม

  python app.py


  หน้าแรกจะเป็น Login

  ถ้าเป็นผู้ใช้ใหม่ → กด Register เพื่อสมัครสมาชิก

  ถ้าเป็นผู้ใช้เดิม → กรอกอีเมลและรหัสผ่านเพื่อเข้าสู่ระบบ

  หลังล็อกอินสำเร็จ → จะเข้าสู่หน้า Dashboard


## กติกาการทำงานร่วมกัน (สรุป)
  - อย่าแก้ `main` โดยตรง
  - สร้าง branch แบบ `feature/<short-name>` เช่น `feature/login`
  - ทำงานเสร็จ → push → เปิด Pull Request
  - ต้องมี reviewer ก่อน merge