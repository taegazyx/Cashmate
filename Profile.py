import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

def create_profile_page(root):
    # Set the theme and color scheme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    # Main frame with mint green background
    profile_frame = ctk.CTkFrame(root, fg_color="#B2F0C1")
    profile_frame.pack(fill=tk.BOTH, expand=True)

    # Bank icon and app name
    bank_label = ctk.CTkLabel(profile_frame, text="🏦", font=ctk.CTkFont(size=60))
    bank_label.pack(pady=(20, 5))
    
    app_name_label = ctk.CTkLabel(
        profile_frame, 
        text="CashMate App", 
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#333333"
    )
    app_name_label.pack(pady=(0, 20))

    # White content frame with rounded corners
    content_frame = ctk.CTkFrame(
        profile_frame,
        fg_color="white",
        corner_radius=15,
        border_width=2,
        border_color="#EAEAEA"
    )
    content_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)

    # User Profile heading
    profile_title = ctk.CTkLabel(
        content_frame,
        text="User Profile",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#333333"
    )
    profile_title.pack(pady=(10, 20))

    # Profile picture frame (circular background)
    profile_frame = ctk.CTkFrame(
        content_frame,
        width=120,
        height=120,
        corner_radius=60,
        fg_color="#E8F4FF"
    )
    profile_frame.pack(pady=10)
    profile_frame.pack_propagate(False)

    # Add a simple avatar label inside the circular frame
    avatar_label = ctk.CTkLabel(
        profile_frame,
        text="👤",
        font=ctk.CTkFont(size=50),
        text_color="#666666"
    )
    avatar_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # User information
    name_label = ctk.CTkLabel(
        content_frame,
        text="Name :",
        font=ctk.CTkFont(size=16),
        text_color="#666666"
    )
    name_label.pack(pady=(20, 5))

    email_label = ctk.CTkLabel(
        content_frame,
        text="Email : xxx@gmail.com",
        font=ctk.CTkFont(size=16),
        text_color="#666666"
    )
    email_label.pack(pady=(0, 20))

    # Buttons
    button_style = {"width": 150, "height": 35, "corner_radius": 8, "font": ctk.CTkFont(size=14)}
    
    # First row of buttons
    button_frame1 = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame1.pack(pady=5)
    
    edit_profile_btn = ctk.CTkButton(
        button_frame1,
        text="Edit Profile",
        fg_color="#666666",
        hover_color="#4D4D4D",
        **button_style
    )
    edit_profile_btn.pack(side=tk.LEFT, padx=5)
    
    change_pass_btn = ctk.CTkButton(
        button_frame1,
        text="Change Password",
        fg_color="#666666",
        hover_color="#4D4D4D",
        **button_style
    )
    change_pass_btn.pack(side=tk.LEFT, padx=5)

    # Second row of buttons
    button_frame2 = ctk.CTkFrame(content_frame, fg_color="transparent")
    button_frame2.pack(pady=5)
    
    privacy_btn = ctk.CTkButton(
        button_frame2,
        text="Privacy & Policy / How to Use",
        fg_color="#666666",
        hover_color="#4D4D4D",
        width=310,
        height=35,
        corner_radius=8,
        font=ctk.CTkFont(size=14)
    )
    privacy_btn.pack(pady=5)
    
    logout_btn = ctk.CTkButton(
        button_frame2,
        text="Logout",
        fg_color="#666666",
        hover_color="#4D4D4D",
        width=310,
        height=35,
        corner_radius=8,
        font=ctk.CTkFont(size=14)
    )
    logout_btn.pack(pady=5)

    # Back to Home button
    back_home_btn = ctk.CTkButton(
        content_frame,
        text="Back to Home",
        fg_color="#666666",
        hover_color="#4D4D4D",
        width=310,
        height=35,
        corner_radius=8,
        font=ctk.CTkFont(size=14)
    )
    back_home_btn.pack(pady=15)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("User Profile")
    root.geometry("400x750")
    
    create_profile_page(root)
    
    root.mainloop()