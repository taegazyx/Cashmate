import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

def open_edit_profile():
    root.destroy()  # Close current window
    import Edit_Profile
    new_window = ctk.CTk()
    Edit_Profile.create_edit_profile_page(new_window)
    new_window.mainloop()

def create_profile_page(root):
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
        text="Back to Home",
        fg_color="white",
        text_color="#000000",
        hover_color="#F5F5F5",
        width=100,
        height=30,
        corner_radius=15,
        font=ctk.CTkFont(size=12, weight="bold")
    )
    back_home_btn.pack(side=tk.LEFT)

    # Bank icon and app name
    # Load and resize bank icon
    bank_image = Image.open("bank_icon.png")
    bank_image = bank_image.resize((90, 90))  # Resize to match previous emoji size
    bank_photo = ImageTk.PhotoImage(bank_image)
    
    bank_label = ctk.CTkLabel(content_container, text="", image=bank_photo)
    bank_label.image = bank_photo  # Keep a reference
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

    # User Profile heading
    profile_title = ctk.CTkLabel(
        content_frame,
        text="User Profile",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#333333"
    )
    profile_title.pack(pady=(10, 20))

    def update_profile_picture(image_label):
        file_path = filedialog.askopenfilename(
            title="Choose Profile Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Open and resize image
                image = Image.open(file_path)
                
                # Convert to RGBA if needed
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                # Make the image square first by cropping to a square
                width, height = image.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = left + size
                bottom = top + size
                image = image.crop((left, top, right, bottom))
                
                # Resize to target size (slightly smaller than frame)
                target_size = (90, 90)
                image = image.resize(target_size, Image.Resampling.LANCZOS)
                
                # No need for mask since we want a square image
                output = image
                
                # Convert to PhotoImage and update label
                photo = ImageTk.PhotoImage(output)
                image_label.configure(image=photo, text="")
                image_label.image = photo  # Keep reference
            except Exception as e:
                print(f"Error loading image: {e}")

    # Outer frame for square background effect
    outer_frame = ctk.CTkFrame(
        content_frame,
        width=120,
        height=120,
        corner_radius=10,
        fg_color="#E8F4FF",
        border_width=2,
        border_color="#D3D3D3"
    )
    outer_frame.pack(pady=10)
    outer_frame.pack_propagate(False)

    # Inner frame for the profile picture with square shape
    profile_frame = ctk.CTkFrame(
        outer_frame,
        width=110,
        height=110,
        corner_radius=8,
        fg_color="#F5F9FF"
    )
    profile_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    profile_frame.pack_propagate(False)

    # Create a label for the profile picture that acts as a button
    profile_pic_label = ctk.CTkLabel(
        profile_frame,
        text="👤\nClick to upload",
        font=ctk.CTkFont(size=24),
        text_color="#666666"
    )
    profile_pic_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Bind click event to the label
    profile_pic_label.bind("<Button-1>", lambda e: update_profile_picture(profile_pic_label))
    
    # Make the label look clickable
    def on_enter(e):
        profile_pic_label.configure(text_color="#333333")
    def on_leave(e):
        profile_pic_label.configure(text_color="#666666")
        
    profile_pic_label.bind("<Enter>", on_enter)
    profile_pic_label.bind("<Leave>", on_leave)
    profile_frame.bind("<Button-1>", lambda e: update_profile_picture(profile_pic_label))

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
        command=open_edit_profile,  # Add command to open Edit Profile page
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
        width=120,
        height=35,
        corner_radius=8,
        font=ctk.CTkFont(size=14)
    )
    logout_btn.pack(pady=5)




if __name__ == "__main__":
    root = ctk.CTk()
    root.title("User Profile")
    root.geometry("400x700")
    
    create_profile_page(root)
    
    root.mainloop()