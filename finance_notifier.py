# finance_notifier.py
import tkinter as tk
from tkinter import messagebox
from typing import Optional

def _show_msgbox(title: str, message: str) -> None:
    """สร้างหน้าต่างชั่วคราวเพื่อแสดง messagebox"""
    # สร้าง root window ชั่วคราวแล้วซ่อนไว้
    # เพื่อให้ messagebox แสดงขึ้นมาตรงกลางจอและอยู่บนสุด
    root = tk.Tk()
    root.withdraw()
    try:
        messagebox.showinfo(title, message, parent=root)
    finally:
        root.destroy() # ทำลายหน้าต่างทิ้งหลังใช้งาน

def _format_money(amount: float, currency: str = "THB") -> str:
    """จัดรูปแบบตัวเลขเป็นสกุลเงิน"""
    return f"{amount:,.2f} {currency}"

def notify_income(amount: float, balance: Optional[float] = None):
    """แจ้งเตือนเมื่อมีรายรับเข้า"""
    title = "💰 Income Added!"
    msg_lines = [f"Amount: {_format_money(amount)}"]
    if balance is not None:
        msg_lines.append(f"\nCurrent Balance: {_format_money(balance)}")
    _show_msgbox(title, "\n".join(msg_lines))

def notify_expense(amount: float, category: str, balance: Optional[float] = None):
    """แจ้งเตือนเมื่อมีรายจ่าย"""
    title = "💸 Expense Logged!"
    msg_lines = [f"Category: {category}", f"Amount: {_format_money(amount)}"]
    if balance is not None:
        msg_lines.append(f"\nCurrent Balance: {_format_money(balance)}")
    _show_msgbox(title, "\n".join(msg_lines))