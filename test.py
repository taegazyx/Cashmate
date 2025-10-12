# app_main.py (ตัวอย่างการเรียก)
from finance_notifier import notify_income, notify_expense, notify_bill_due, notify_budget_overrun, notify_transaction

# เมื่อกด 'รับ'
notify_income(amount=1500, category="งานเสริม", note="โอนจากลูกค้า A", balance=8450)

# เมื่อกด 'จ่าย'
notify_expense(amount=220, category="อาหาร", note="ข้าวเที่ยง", balance=8230)

# หรือใช้แบบ generic
notify_transaction(trx_type="income", amount=300, category="คืนภาษี", balance=8530)

# เตือนบิล
notify_bill_due(bill_name="ค่าน้ำ", due_date="2025-10-15", amount=180, days_left=3)

# เตือนเกินงบ
notify_budget_overrun(category="บันเทิง", spent=2500, limit_amount=2000)
