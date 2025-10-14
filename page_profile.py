# page_profile.py
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog
import os

# --- 1. สร้าง Class เพื่อห่อหุ้มโค้ดทั้งหมด ---
class ProfilePage:
    # --- 2. สร้าง __init__ ที่รับ parent (content_frame จากไฟล์หลัก) ---
    def __init__(self, parent):
        # การตั้งค่า Theme ควรทำครั้งเดียวในไฟล์ main_app.py
        # ctk.set_appearance_mode("light")
        # ctk.set_default_color_theme("green")

        # --- 3. เปลี่ยน parent เดิม (root) ให้เป็น parent ที่รับเข้ามา ---
        self.main_frame = ctk.CTkFrame(parent, fg_color="#B2F0C1")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 4. ย้ายโค้ด UI เดิมทั้งหมดมาไว้ตรงนี้ ---
        content_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ... (โค้ดส่วน Bank icon, App name, Content frame เหมือนเดิม) ...
        bank_label = ctk.CTkLabel(content_container, text="🏦", font=ctk.CTkFont(size=60))
        bank_label.pack(pady=(20, 5))
        app_name_label = ctk.CTkLabel(content_container, text="CashMate App", font=ctk.CTkFont(size=24, weight="bold"), text_color="#333333")
        app_name_label.pack(pady=(0, 20))
        content_frame = ctk.CTkFrame(content_container, fg_color="white", corner_radius=15, border_width=2, border_color="#EAEAEA")
        content_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)
        profile_title = ctk.CTkLabel(content_frame, text="User Profile", font=ctk.CTkFont(size=28, weight="bold"), text_color="#333333")
        profile_title.pack(pady=(10, 20))

        # ... (โค้ดส่วน Profile Picture Frame เหมือนเดิม) ...
        outer_frame = ctk.CTkFrame(content_frame, width=140, height=140, corner_radius=70, fg_color="#E8F4FF", border_width=2, border_color="#D3D3D3")
        outer_frame.pack(pady=10)
        outer_frame.pack_propagate(False)
        profile_frame = ctk.CTkFrame(outer_frame, width=130, height=130, corner_radius=65, fg_color="#F5F9FF")
        profile_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        profile_frame.pack_propagate(False)

        # Label for profile picture
        self.profile_pic_label = ctk.CTkLabel(profile_frame, text="👤\nClick to upload", font=ctk.CTkFont(size=30), text_color="#666666")
        self.profile_pic_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Bind events
        self.profile_pic_label.bind("<Button-1>", lambda e: self.update_profile_picture(self.profile_pic_label))
        self.profile_pic_label.bind("<Enter>", self.on_enter)
        self.profile_pic_label.bind("<Leave>", self.on_leave)
        profile_frame.bind("<Button-1>", lambda e: self.update_profile_picture(self.profile_pic_label))

        # ... (โค้ดส่วน User Information และ Buttons เหมือนเดิม) ...
        name_label = ctk.CTkLabel(content_frame, text="Name :", font=ctk.CTkFont(size=16), text_color="#666666")
        name_label.pack(pady=(20, 5))
        email_label = ctk.CTkLabel(content_frame, text="Email : xxx@gmail.com", font=ctk.CTkFont(size=16), text_color="#666666")
        email_label.pack(pady=(0, 20))

        # Buttons
        button_style = {"width": 150, "height": 35, "corner_radius": 8, "font": ctk.CTkFont(size=14)}
        button_frame1 = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame1.pack(pady=5)
        edit_profile_btn = ctk.CTkButton(button_frame1, text="Edit Profile", fg_color="#666666", hover_color="#4D4D4D", **button_style)
        edit_profile_btn.pack(side=tk.LEFT, padx=5)
        change_pass_btn = ctk.CTkButton(button_frame1, text="Change Password", fg_color="#666666", hover_color="#4D4D4D", **button_style)
        change_pass_btn.pack(side=tk.LEFT, padx=5)

        button_frame2 = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame2.pack(pady=5)
        privacy_btn = ctk.CTkButton(button_frame2, text="Privacy & Policy / How to Use", fg_color="#666666", hover_color="#4D4D4D", width=310, height=35, corner_radius=8, font=ctk.CTkFont(size=14))
        privacy_btn.pack(pady=5)
        logout_btn = ctk.CTkButton(button_frame2, text="Logout", fg_color="#666666", hover_color="#4D4D4D", width=310, height=35, corner_radius=8, font=ctk.CTkFont(size=14))
        logout_btn.pack(pady=5)
        
        # --- 6. ลบปุ่ม "Back to Home" ออกไป ---
        # เนื่องจากในแอปหลักของเรามี Sidebar สำหรับนำทางอยู่แล้ว
        # จึงไม่จำเป็นต้องมีปุ่มนี้ซ้ำซ้อน

    # --- 5. เปลี่ยนฟังก์ชันเดิม ให้เป็นเมธอดของคลาส (เพิ่ม self) ---
    def update_profile_picture(self, image_label):
        file_path = filedialog.askopenfilename(
            title="Choose Profile Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                image = Image.open(file_path)
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                width, height = image.size
                size = min(width, height)
                left, top = (width - size) // 2, (height - size) // 2
                right, bottom = left + size, top + size
                image = image.crop((left, top, right, bottom))
                
                target_size = (110, 110)
                image = image.resize(target_size, Image.Resampling.LANCZOS)
                
                mask = Image.new('L', target_size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, target_size[0], target_size[1]), fill=255)
                
                output = Image.new('RGBA', target_size, (0, 0, 0, 0))
                output.paste(image, (0, 0), mask)
                
                photo = ImageTk.PhotoImage(output)
                image_label.configure(image=photo, text="")
                image_label.image = photo
            except Exception as e:
                print(f"Error loading image: {e}")

    def on_enter(self, e):
        self.profile_pic_label.configure(text_color="#333333")

    def on_leave(self, e):
        self.profile_pic_label.configure(text_color="#666666")

# --- 7. ลบส่วน if __name__ == "__main__": ออกไป ---
# เพราะไฟล์นี้จะไม่ได้ถูกรันโดยตรงอีกแล้ว แต่จะถูก import ไปใช้