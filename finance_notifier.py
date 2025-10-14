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
    """จัดรูปแบบตัวเลขให้เป็นสกุลเงิน"""
    try:
        return f"{amount:,.2f} {currency}"
    except Exception:
        return f"{amount} {currency}"

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
            # ใช้ System Notification พร้อม Timeout 10 วินาที
            notification.notify(title=title, message=message, timeout=timeout_sec)
            return
        except Exception:
            pass 
    
    # ถ้า plyer ใช้ไม่ได้ (หรือไม่มี), จะใช้ messagebox ซึ่งไม่สามารถกำหนด timeout ได้
    _show_msgbox(title, message)

# ----------------------------------------------------------------------
# ---------- ฟังก์ชันแจ้งเตือนเฉพาะรายการทางการเงินหลัก ----------
# ----------------------------------------------------------------------

def notify_income(amount: float,
                  category: str,
                  note: Optional[str] = None, # 👈 ตัวแปรนี้ยังคงรับได้ แต่จะไม่ถูกนำไปใช้
                  balance: Optional[float] = None,
                  currency: str = "THB") -> None:
    """
    เรียกเมื่อ 'รับเงิน' สำเร็จ (แจ้งเตือน รายรับ และยอดคงเหลือ)
    """
    title = "💰 บันทึกรายรับแล้ว"
    # 🔴 ลบบรรทัดที่เพิ่มหมายเหตุออก
    msg = [f"✅ หมวด: {category}", f"💸 จำนวน: {_format_money(amount, currency)}"]
    
    if balance is not None:
        msg.append(f"📊 ยอดคงเหลือ: {_format_money(balance, currency)}")
        
    _notify(title, "\n".join(msg)) 

def notify_expense(amount: float,
                    category: str,
                    note: Optional[str] = None,
                    balance: Optional[float] = None,
                    currency: str = "THB") -> None:
    """
    เรียกเมื่อ 'จ่ายเงิน' สำเร็จ (แจ้งเตือน รายจ่าย และยอดคงเหลือ)
    """
    title = "💸 บันทึกรายจ่ายแล้ว"
    msg = [f"❌ หมวด: {category}", f"📉 จำนวน: {_format_money(amount, currency)}"]
    
    # 🟢 รายจ่ายยังคงแสดงหมายเหตุ
    if note:
        msg.append(f"📝 รายการ: {note}")
        
    if balance is not None:
        msg.append(f"📊 ยอดคงเหลือ: {_format_money(balance, currency)}")
        
    _notify(title, "\n".join(msg))

def notify_transaction(trx_type: str,
                        amount: float,
                        category: str,
                        note: Optional[str] = None,
                        balance: Optional[float] = None,
                        currency: str = "THB") -> None:
    """เวอร์ชัน generic"""
    if trx_type.lower() == "income":
        # เมื่อเรียก notify_income จะไม่มีหมายเหตุตามการแก้ไขด้านบน
        return notify_income(amount, category, note, balance, currency)
    elif trx_type.lower() == "expense":
        return notify_expense(amount, category, note, balance, currency)
    
    # กรณีประเภทรายการไม่ชัดเจน
    title = "📢 บันทึกรายการ"
    msg = [f"ประเภท: {trx_type}", f"หมวด: {category}", f"จำนวน: {_format_money(amount, currency)}"]
    
    if note:
        msg.append(f"หมายเหตุ: {note}")
        
    if balance is not None:
        msg.append(f"ยอดคงเหลือ: {_format_money(balance, currency)}")
        
    _notify(title, "\n".join(msg))