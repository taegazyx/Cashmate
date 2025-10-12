from typing import Optional

# พยายามใช้ System Notification ถ้ามี plyer
try:
    from plyer import notification
    HAVE_PLYER = True
except Exception:
    HAVE_PLYER = False

import tkinter as tk
from tkinter import messagebox

def _format_money(amount: float, currency: str = "THB") -> str:
    try:
        return f"{amount:,.2f} {currency}"
    except Exception:
        return f"{amount} {currency}"

def _show_msgbox(title: str, message: str) -> None:
    
    root = tk.Tk()
    root.withdraw()
    try:
        messagebox.showinfo(title, message, parent=root)
    finally:
        root.destroy()

def _notify(title: str, message: str, timeout_sec: int = 6) -> None:
    """
    แสดงการแจ้งเตือน
    - ถ้ามี plyer: ใช้ System Notification
    - ถ้าไม่มี: ใช้ messagebox
    """
    if HAVE_PLYER:
        try:
            notification.notify(title=title, message=message, timeout=timeout_sec)
            return
        except Exception:
            pass
    _show_msgbox(title, message)

# ---------- ฟังก์ชันที่จะเรียกจากระบบหลัก ----------

def notify_income(amount: float,
                  category: str,
                  note: Optional[str] = None,
                  balance: Optional[float] = None,
                  currency: str = "THB") -> None:
    """
    เรียกเมื่อ 'รับเงิน' สำเร็จจากระบบหลัก
    """
    title = "รับเงินเข้าแล้ว "
    msg = [f"หมวด: {category}", f"จำนวน: {_format_money(amount, currency)}"]
    if note:
        msg.append(f"หมายเหตุ: {note}")
    if balance is not None:
        msg.append(f"ยอดคงเหลือปัจจุบัน: {_format_money(balance, currency)}")
    _notify(title, "\n".join(msg))

def notify_expense(amount: float,
                   category: str,
                   note: Optional[str] = None,
                   balance: Optional[float] = None,
                   currency: str = "THB") -> None:
    """
    เรียกเมื่อ 'จ่ายเงิน' สำเร็จจากระบบหลัก
    """
    title = "บันทึกรายจ่ายแล้ว "
    msg = [f"หมวด: {category}", f"จำนวน: {_format_money(amount, currency)}"]
    if note:
        msg.append(f"หมายเหตุ: {note}")
    if balance is not None:
        msg.append(f"ยอดคงเหลือปัจจุบัน: {_format_money(balance, currency)}")
    _notify(title, "\n".join(msg))

def notify_bill_due(bill_name: str,
                    due_date: str,
                    amount: Optional[float] = None,
                    days_left: Optional[int] = None,
                    currency: str = "THB") -> None:
    """
    เรียกจากระบบหลักเมื่ออยากเตือนบิล
    """
    title = "เตือนชำระบิล "
    msg = [f"บิล: {bill_name}", f"กำหนด: {due_date}"]
    if amount is not None:
        msg.append(f"จำนวน: {_format_money(amount, currency)}")
    if days_left is not None:
        if days_left == 0:
            msg.append("ครบกำหนดวันนี้")
        elif days_left > 0:
            msg.append(f"จะครบใน {days_left} วัน")
        else:
            msg.append(f"เกินกำหนด {-days_left} วัน")
    _notify(title, "\n".join(msg))

def notify_budget_overrun(category: str,
                          spent: float,
                          limit_amount: float,
                          currency: str = "THB") -> None:
    """
    เรียกเมื่อระบบหลักตรวจพบว่าใช้เกินงบ
    """
    title = "ใช้เกินงบหมวดนี้ ⚠️"
    msg = [
        f"หมวด: {category}",
        f"ใช้ไป: {_format_money(spent, currency)}",
        f"งบ: {_format_money(limit_amount, currency)}"
    ]
    _notify(title, "\n".join(msg))

def notify_transaction(trx_type: str,
                       amount: float,
                       category: str,
                       note: Optional[str] = None,
                       balance: Optional[float] = None,
                       currency: str = "THB") -> None:
    """
    เวอร์ชัน generic: trx_type = 'income' หรือ 'expense'
    """
    if trx_type.lower() == "income":
        return notify_income(amount, category, note, balance, currency)
    return notify_expense(amount, category, note, balance, currency)
