import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

def back_to_profile():
    root.destroy()  # Close current window
    import Profile
    new_window = ctk.CTk()
    new_window.geometry("900x600")  # Set consistent window size
    Profile.create_profile_page(new_window)
    new_window.mainloop()

def create_change_password_page(root):
    # Set the theme and color scheme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    # Main frame with green background
    main_frame = ctk.CTkFrame(root, fg_color="#B2F0C1")  # Medium green color
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Content container to help with positioning
    content_container = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Top navigation frame
    nav_frame = ctk.CTkFrame(content_container, fg_color="transparent")
    nav_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Back to Home button - placed at top left
    back_home_btn = ctk.CTkButton(
        nav_frame,
        text="Back",
        fg_color="white",
        text_color="#000000",
        hover_color="#F5F5F5",
        width=100,
        height=30,
        corner_radius=15,
        font=ctk.CTkFont(size=12, weight="bold"),
        command=back_to_profile
    )
    back_home_btn.pack(side=tk.LEFT)

    # Bank icon and app name
    try:
        bank_image = Image.open("bank_icon.png")
        bank_image = bank_image.resize((90, 90))
        bank_photo = ImageTk.PhotoImage(bank_image)
        bank_label = ctk.CTkLabel(content_container, text="", image=bank_photo)
        bank_label.image = bank_photo
    except FileNotFoundError:
        bank_label = ctk.CTkLabel(content_container, text="🏦", font=ctk.CTkFont(size=72))
    bank_label.pack(pady=(5, 5))
    
    app_name_label = ctk.CTkLabel(
        content_container, 
        text="CashMate App", 
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#333333"
    )
    app_name_label.pack(pady=(0, 20))

    # White content frame with rounded corners
    content_frame = ctk.CTkFrame(
        content_container,
        fg_color="white",
        corner_radius=15,
        border_width=2,
        border_color="#EAEAEA"
    )
    content_frame.pack(pady=20, padx=20, ipadx=20, ipady=20)

    # Change Password heading
    password_title = ctk.CTkLabel(
        content_frame,
        text="Change Password",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#333333"
    )
    password_title.pack(pady=(10, 30))

    # Password Entry Fields
    entry_style = {"width": 280, "height": 40, "corner_radius": 8}
    
    # Current Password
    current_pass_label = ctk.CTkLabel(
        content_frame,
        text="Current Password",
        font=ctk.CTkFont(size=14),
        text_color="#666666"
    )
    current_pass_label.pack(anchor="w", padx=20, pady=(0, 5))
    
    current_pass_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Enter current password",
        show="•",
        **entry_style
    )
    current_pass_entry.pack(pady=(0, 15))

    # New Password
    new_pass_label = ctk.CTkLabel(
        content_frame,
        text="New Password",
        font=ctk.CTkFont(size=14),
        text_color="#666666"
    )
    new_pass_label.pack(anchor="w", padx=20, pady=(0, 5))
    
    new_pass_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Enter new password",
        show="•",
        **entry_style
    )
    new_pass_entry.pack(pady=(0, 15))

    # Confirm New Password
    confirm_pass_label = ctk.CTkLabel(
        content_frame,
        text="Confirm New Password",
        font=ctk.CTkFont(size=14),
        text_color="#666666"
    )
    confirm_pass_label.pack(anchor="w", padx=20, pady=(0, 5))
    
    confirm_pass_entry = ctk.CTkEntry(
        content_frame,
        placeholder_text="Confirm new password",
        show="•",
        **entry_style
    )
    confirm_pass_entry.pack(pady=(0, 30))

    # Save Button
    save_btn = ctk.CTkButton(
        content_frame,
        text="Save Changes",
        fg_color="#666666",
        hover_color="#4D4D4D",
        width=200,
        height=40,
        corner_radius=8,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    save_btn.pack(pady=10)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Change Password")
    root.geometry("900x600")
    
    create_change_password_page(root)
    
    root.mainloop()
 