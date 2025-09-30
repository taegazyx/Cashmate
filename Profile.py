import tkinter as tk
from tkinter import ttk

def create_profile_page(root):
    """
    สร้างหน้าต่างโปรไฟล์ผู้ใช้
    """
    profile_frame = tk.Frame(root, bg="#B2F0C1")  # พื้นหลังสีฟ้าอ่อน
    profile_frame.pack(fill=tk.BOTH, expand=True)

    # --- ส่วนหัว (โลโก้และชื่อแอป) ---
    app_logo_label = tk.Label(profile_frame, text="🏦", font=("Arial", 60), bg="#B2F0C1")
    app_logo_label.pack(pady=(20, 5))
    
    app_name_label = tk.Label(profile_frame, text="CashMate App", font=("Arial", 16, "bold"), bg="#B2EBF2")
    app_name_label.pack(pady=(0, 20))

    # --- กรอบสำหรับเนื้อหาหลัก (User Profile) ---
    content_frame = tk.Frame(profile_frame, bg="white", bd=2, relief="groove")
    content_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)
    
    # เพิ่มโค้งมนให้กับกรอบ
    content_frame.config(highlightbackground="gray", highlightthickness=1, borderwidth=5)

    # หัวข้อ "User Profile"
    profile_title = tk.Label(content_frame, text="User Profile", font=("Arial", 24, "bold"), bg="white")
    profile_title.pack(pady=(10, 20))

    # --- รูปภาพโปรไฟล์ (ใช้ placeholder เป็นวงกลม) ---
    profile_canvas = tk.Canvas(content_frame, width=150, height=150, bg="white", highlightthickness=0)
    profile_canvas.pack(pady=10)
    profile_canvas.create_oval(10, 10, 140, 140, fill="#E6F2FF", outline="#D3D3D3")
    
    # เพิ่มรูปภาพผู้ใช้ (ในโค้ดนี้ใช้เป็นตัวอย่าง)
    # หากต้องการใช้รูปภาพจริง:
    # try:
    #     user_img = tk.PhotoImage(file="path/to/your/image.png")
    #     profile_canvas.create_image(75, 75, image=user_img)
    # except tk.TclError:
    #     pass # จัดการในกรณีที่หารูปภาพไม่พบ

    # --- ข้อมูลโปรไฟล์ ---
    name_label = tk.Label(content_frame, text="Name :", font=("Arial", 14), bg="white")
    name_label.pack(pady=(20, 0))
    
    email_label = tk.Label(content_frame, text="Email : xxx@gmail.com", font=("Arial", 14), bg="white")
    email_label.pack(pady=(5, 20))

    # --- ปุ่มต่างๆ ---
    # ใช้ ttk.Button เพื่อให้มีสไตล์ที่ดูทันสมัยขึ้น
    button_style = ttk.Style()
    button_style.configure("TButton", font=("Arial", 12), padding=10, background="#666666", foreground="white")

    button_frame1 = tk.Frame(content_frame, bg="white")
    button_frame1.pack(pady=5)
    
    edit_button = ttk.Button(button_frame1, text="Edit Profile")
    edit_button.pack(side=tk.LEFT, padx=10)
    
    change_pass_button = ttk.Button(button_frame1, text="Change Password")
    change_pass_button.pack(side=tk.LEFT, padx=10)

    button_frame2 = tk.Frame(content_frame, bg="white")
    button_frame2.pack(pady=5)
    
    privacy_button = ttk.Button(button_frame2, text="Privacy & Policy / How to Use")
    privacy_button.pack(side=tk.LEFT, padx=10)
    
    logout_button = ttk.Button(button_frame2, text="Logout")
    logout_button.pack(side=tk.LEFT, padx=10)

    # --- ปุ่ม "Back to Home" ---
    back_home_button = tk.Button(profile_frame, text="Back to Home", font=("Arial", 16), bg="#6A5ACD", fg="white", relief="raised", bd=3)
    back_home_button.pack(pady=20, ipadx=50, ipady=10)
    
    # ทำให้ปุ่มมีโค้งมน
    back_home_button.config(border=5, relief="raised", highlightbackground="#6A5ACD", highlightcolor="#6A5ACD")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("User Profile")
    root.geometry("400x700")  # กำหนดขนาดหน้าต่างเริ่มต้น
    
    create_profile_page(root)
    
    root.mainloop()