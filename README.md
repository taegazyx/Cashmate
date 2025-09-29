# Finance Tracker (Python + CustomTkinter + MariaDB)

## คำอธิบาย
โปรแกรมบันทึกรายรับ–รายจ่าย สำหรับเรียนรู้และใช้งานเป็นทีม

## ขั้นตอนติดตั้ง (สำหรับนักพัฒนา)
1. Clone repo:
git clone https://github.com/Thanapat68030116/Project-Personal-income-and-expenses
cd Project-Personal-income-and-expenses

r
Copy code
2. สร้าง virtualenv และ activate:
- mac/linux:
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
3. ติดตั้งแพ็กเกจ:
pip install -r requirements.txt

markdown
Copy code
4. เตรียม `.env`:
- คัดลอก `.env.example` → `.env` แล้วแก้ค่าให้เป็นของเครื่องคุณ
5. สร้างฐานข้อมูล:
- import `database_schema.sql` ลง MariaDB (phpMyAdmin / CLI)
6. รันโปรแกรม:
python main.py

markdown
Copy code

## กติกาการทำงานร่วมกัน (สรุป)
- อย่าแก้ `main` โดยตรง
- สร้าง branch แบบ `feature/<short-name>` เช่น `feature/login`
- ทำงานเสร็จ → push → เปิด Pull Request
- ต้องมี reviewer ก่อน merge