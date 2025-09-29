import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("650x450")
        self.root.configure(bg="#e8f5e9")  # โทนสีเขียวอ่อน

        # ----- Header -----
        header_frame = tk.Frame(root, bg="#66bb6a", height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame,
                 text="📊 History Report",
                 font=("Arial", 18, "bold"),
                 bg="#66bb6a", fg="white").pack(pady=10)

        # ----- Data -----
        self.expenses = []  # [ (date, category, amount) ]
        self.categories = ["อาหาร", "ค่ารถ", "ช้อปปิ้ง", "อื่นๆ"]

        # ----- Input Section -----
        frame_input = tk.Frame(self.root, bg="#a5d6a7", pady=10)
        frame_input.pack(fill="x")

        tk.Label(frame_input, text="วันที่:", bg="#a5d6a7").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(frame_input, width=12, background="green", foreground="white",
                                    borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="หมวดหมู่:", bg="#a5d6a7").grid(row=0, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(frame_input, textvariable=self.category_var,
                                           values=self.categories, state="readonly")
        self.category_combo.grid(row=0, column=3, padx=5)
        self.category_combo.current(0)

        tk.Label(frame_input, text="จำนวนเงิน:", bg="#a5d6a7").grid(row=0, column=4, padx=5, pady=5)
        self.amount_entry = tk.Entry(frame_input)
        self.amount_entry.grid(row=0, column=5, padx=5)

        self.btn_add = tk.Button(frame_input, text="บันทึก", command=self.add_expense,
                                 bg="#388e3c", fg="white")
        self.btn_add.grid(row=0, column=6, padx=5)

        # ----- History Table -----
        frame_table = tk.Frame(self.root, bg="#e8f5e9")
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("วันที่", "หมวดหมู่", "จำนวนเงิน")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_var.get()
        amount = self.amount_entry.get().strip()

        try:
            amount = float(amount)
            self.expenses.append((date, category, amount))
            self.tree.insert("", "end", values=(date, category, f"{amount:.2f}"))
            self.amount_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "กรุณากรอกจำนวนเงิน เช่น +100 หรือ -50")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
