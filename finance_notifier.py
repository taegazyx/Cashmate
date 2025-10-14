# finance_notifier.py (ฉบับอัปเกรดด้วย Plyer)
from typing import Optional
import tkinter as tk
from tkinter import messagebox

# พยายามใช้ System Notification ถ้ามี plyer
try:
    from plyer import notification
    HAVE_PLYER = True
    print("Plyer library found. System notifications will be used.")
except ImportError:
    HAVE_PLYER = False
    print("Plyer library not found. Falling back to tkinter messagebox.")

def _format_money(amount: float, currency: str = "THB") -> str:
    """จัดรูปแบบตัวเลขให้เป็นสกุลเงิน"""
    return f"{amount:,.2f} {currency}"

def _show_msgbox(title: str, message: str) -> None:
    """แสดงกล่องข้อความของ Tkinter (fallback)"""
    root = tk.Tk()
    root.withdraw()
    try:
        messagebox.showinfo(title, message, parent=root)
    finally:
        root.destroy()

def _notify(title: str, message: str, timeout_sec: int = 10) -> None:
    """
    แสดงการแจ้งเตือน
    - ถ้ามี plyer: ใช้ System Notification (หายไปเองใน 10 วินาที)
    - ถ้าไม่มี: ใช้ messagebox (ต้องกด OK เพื่อปิด)
    """
    if HAVE_PLYER:
        try:
            notification.notify(title=title, message=message, timeout=timeout_sec)
            return
        except Exception as e:
            print(f"Plyer notification failed: {e}. Falling back to messagebox.")
            pass
    _show_msgbox(title, message)

# ---------- ฟังก์ชันแจ้งเตือนหลัก (ปรับปรุงเล็กน้อย) ----------

def notify_income(amount: float, balance: Optional[float] = None):
    """
    แจ้งเตือนเมื่อ 'รับเงิน' สำเร็จ
    """
    title = "💰 Income Recorded"
    msg = [f"Amount: {_format_money(amount)}"]
    if balance is not None:
        msg.append(f"Current Balance: {_format_money(balance)}")
    _notify(title, "\n".join(msg))

def notify_expense(amount: float, category: str, note: Optional[str] = None, balance: Optional[float] = None):
    """
    แจ้งเตือนเมื่อ 'จ่ายเงิน' สำเร็จ
    """
    title = "💸 Expense Recorded"
    msg = [f"Category: {category}", f"Amount: {_format_money(amount)}"]
    if note:
        msg.append(f"Item: {note}") # ใช้ 'Item' หรือ 'Description' ก็ได้
    if balance is not None:
        msg.append(f"Current Balance: {_format_money(balance)}")
    _notify(title, "\n".join(msg))