# CASHMATH – ระบบ Login/Register + Dashboard

# โปรแกรมนี้เป็นแอปพลิเคชัน GUI สำหรับ ล็อกอิน / ลงทะเบียนผู้ใช้ โดยเชื่อมต่อกับฐานข้อมูล MariaDB และใช้ bcrypt ในการเข้ารหัสรหัสผ่าน

# สร้างด้วย Python + CustomTkinter

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


# สุดท้าย วิธีการใช้งาน

  รันโปรแกรม

  python app.py


  หน้าแรกจะเป็น Login

  ถ้าเป็นผู้ใช้ใหม่ → กด Register เพื่อสมัครสมาชิก

  ถ้าเป็นผู้ใช้เดิม → กรอกอีเมลและรหัสผ่านเพื่อเข้าสู่ระบบ

  หลังล็อกอินสำเร็จ → จะเข้าสู่หน้า Dashboard

## คำสั่ง git ต่างๆ
  1.  git init -สร้าง repository
  2.  git add ชื่อไฟล์ หรือใส่ . จะแอดไฟล์ทั้งหมด
  3.  git commit -m "ข้อความ" -commit ข้อความทุกครั้งที่กระทำอะไรก็ตามกับไฟล์
  4.  git rm <ชื่อไฟล์> -ลบไฟล์ออกจาก git
  5.  git log -ดูประวัติแบบเต็ม
  6.  git log --oneline -ดูประวัติแบบสั้นๆ
  7.  git status -เช็คไฟล์ว่าถูก track หรือยัง
  8.  git clone https://github.com/taegazyx/Cashmate 
  9.  git mv เก่า ใหม่ -เปลี่ยนชื่อหรือย้ายไฟล์
  10. git branch -เช็คว่าตัวเองอยู่ branch ไหน
  11. git checkout branch -สลับไป branch ที่ต้องการ
  12. git checkout -b branch -สร้าง branch ใหม่ + สลับไปด้วย ***กรณีไม่เคยสร้าง branch แยกเลย
  13. git merge branch -รวม branch อื่นเข้ามาที่ branch ปัจจุบัน 
  14. git remote -v → ดู remote ที่เชื่อมอยู่
  15. git remote add origin https://github.com/taegazyx/Cashmate → เพิ่ม remote
  16. git push origin branch → อัปโหลด branch ไปที่ remote
  17. git push -u origin branch → อัปโหลด + ตั้งให้ track กับ remote
  18. git pull origin branch → ดึงการเปลี่ยนแปลงจาก remot

  ## ถ้าเกิดทำไม่เป็นโปรดอ่านนะจ้ะ

  1. สร้าง repo พิมพ์ git init ไฟล์เราถ้ามีอย่าเพิ่ง add นะไว้ใน add ใน branch ของตัวเอง 
  2. พิมพ์ใน terminal  git remote add origin https://github.com/taegazyx/Cashmate
  3. เช็คว่า remote แล้วมั้ย git remote -v
  4. ถ้า remote แล้วจะเป็นลิงก์ github หลังจากนั้นก็ใช้ git pull origin main ก่อนมาเก็บไว้
  5. หลังจากนั้นก็ git pull origin (feature/ของแต่ละคนนะ) เช่น git pull origin feature/notification ถ้ามี branch ของเราอยู่บน github แล้ว 
  6. ถ้ายังไม่มีก็สร้าง branch เรามาโดยพิมพ์ git checkout -b (feature/ของแต่ละคนนะ) ตัวอย่างเช่น git checkout -b feature/notification
  7. เราก็แอดไฟล์หรือโค้ดเข้า branch ตัวเองเลย เช็คด้วย git status
  8. ถ้าเราพอใจแล้วก็ส่งโค้ดขึ้น github โดยพิมพ์  git push -u origin ชื่อbranch *กรณีครั้งแรกเพื่อให้ track กับ remote
  9. จากนั้นไม่ต้องพิมพ์คำสั่งนี้แล้ว ให้พิมพ์ git push origin ชื่อbranch ทุกครั้งที่อัปโหลด หรือจะพิมพ์ git push
  10. และพิมพ์ git pull origin ชื่อbranch ทุกครั้งที่ต้องการดึงข้อมูลให้โค้ดเป็นปัจจุบัน หรือจะพิมพ์ git pull 
  11. **ข้อควรละวังนะถ้าจะดึง branch ไหนให้ทำใน branch นั้น เช่น จะดึง branch feature/home บน github บนเครื่องเราก็ต้องอยู่ branch feature/home ด้วย**


## กติกาการทำงานร่วมกัน (สรุป)
  - อย่าแก้ `main` โดยตรง
  - สร้าง branch แบบ `feature/<short-name>` เช่น `feature/login`
  - ทำงานเสร็จ → push → เปิด Pull Request
  - ต้องมี reviewer ก่อน merge