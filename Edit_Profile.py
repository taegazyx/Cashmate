import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

def back_to_profile():
    root.destroy()  # Close current window
    import Profile
    new_window = ctk.CTk()
    Profile.create_profile_page(new_window)
    new_window.mainloop()

def create_edit_profile_page(root):
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
        font=ctk.CTkFont(size=12, weight="bold"),
        command=back_to_profile  # Add command to go back to profile page
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

    # Edit Profile heading
    profile_title = ctk.CTkLabel(
        content_frame,
        text="Edit Profile",
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
                image = Image.open(file_path)
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                width, height = image.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = left + size
                bottom = top + size
                image = image.crop((left, top, right, bottom))
                
                target_size = (90, 90)
                image = image.resize(target_size, Image.Resampling.LANCZOS)
                
                output = image
                photo = ImageTk.PhotoImage(output)
                image_label.configure(image=photo, text="")
                image_label.image = photo
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
    
    profile_pic_label.bind("<Button-1>", lambda e: update_profile_picture(profile_pic_label))
    
    def on_enter(e):
        profile_pic_label.configure(text_color="#333333")
    def on_leave(e):
        profile_pic_label.configure(text_color="#666666")
    
    profile_pic_label.bind("<Enter>", on_enter)
    profile_pic_label.bind("<Leave>", on_leave)
    profile_frame.bind("<Button-1>", lambda e: update_profile_picture(profile_pic_label))

    # User information entry fields
    entry_style = {"font": ctk.CTkFont(size=14), "width": 300, "height": 35, "corner_radius": 8}
    
    # Name
    name_entry = ctk.CTkEntry(content_frame, placeholder_text="Name", **entry_style)
    name_entry.pack(pady=(10, 5))
    name_entry.insert(0, "User Name") # Pre-fill with a placeholder name

    # Email
    email_entry = ctk.CTkEntry(content_frame, placeholder_text="Email", **entry_style)
    email_entry.pack(pady=5)
    email_entry.insert(0, "xxx@gmail.com") # Pre-fill with a placeholder email
    
    # Phone Number
    phone_entry = ctk.CTkEntry(content_frame, placeholder_text="Phone Number", **entry_style)
    phone_entry.pack(pady=5)
    
    # Address
    address_entry = ctk.CTkEntry(content_frame, placeholder_text="Address", **entry_style)
    address_entry.pack(pady=5)

    # Save Changes button
    def save_changes():
        # This function would contain the logic to save the updated user information
        # For this example, we'll just print the new data.
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        
        print(f"Saving changes...")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Address: {address}")

    save_btn = ctk.CTkButton(
        content_frame,
        text="Save Changes",
        fg_color="#4CAF50",
        hover_color="#45a049",
        width=200,
        height=40,
        corner_radius=10,
        font=ctk.CTkFont(size=16, weight="bold"),
        command=save_changes
    )
    save_btn.pack(pady=(20, 10))

# Main application window setup
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Edit Profile")
    root.geometry("400x700")
    
    create_edit_profile_page(root)
    
    root.mainloop()