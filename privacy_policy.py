import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

def back_to_profile():
    root.destroy()  # Close current window
    import Profile
    new_window = ctk.CTk()
    new_window.geometry("900x600")  # Set consistent window size
    Profile.create_profile_page(new_window)
    new_window.mainloop()

def create_privacy_page(root):
    # Set the theme and color scheme
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    # Set up background image
    try:
        bg_image = Image.open("background.jpg")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        print("Background image not found")

    # Main frame with transparent background
    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Content container to help with positioning
    content_container = ctk.CTkFrame(main_frame, fg_color="transparent")
    content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Top navigation frame
    nav_frame = ctk.CTkFrame(content_container, fg_color="transparent")
    nav_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Back to Profile button
    back_profile_btn = ctk.CTkButton(
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
    back_profile_btn.pack(side=tk.LEFT)

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
    content_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    # Create a canvas with scrollbar for the content
    canvas = ctk.CTkCanvas(
        content_frame,
        bg="white",
        highlightthickness=0
    )
    scrollbar = ctk.CTkScrollbar(content_frame, command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the scrollbar and canvas
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Create a window in the canvas for the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Privacy Policy Section
    privacy_title = ctk.CTkLabel(
        scrollable_frame,
        text="Privacy Policy",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#333333"
    )
    privacy_title.pack(pady=(20, 10), padx=(320, 0))

    privacy_text = """
1. Information Collection
   • We collect basic user information for account creation
   • Financial data is stored securely and encrypted
   • We do not share your personal information with third parties 

2. Data Security
   • Your data is protected using industry-standard encryption
   • Regular security updates and monitoring
   • Secure login and authentication processes

3. User Rights
   • You can access and update your personal information
   • Option to delete your account and associated data
   • Control over privacy settings and notifications
    """

    # Create a frame for the privacy text to allow for proper left alignment
    privacy_text_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    privacy_text_frame.pack(fill=tk.X, pady=10, padx=20)
    
    privacy_label = ctk.CTkLabel(
        privacy_text_frame,
        text=privacy_text,
        font=ctk.CTkFont(size=14),
        text_color="#666666",
        justify="left",
        anchor="w"
    )
    privacy_label.pack(fill=tk.X, anchor="w")

    # How to Use Section
    usage_title = ctk.CTkLabel(
        scrollable_frame,
        text="How to Use CashMate",
        font=ctk.CTkFont(size=24, weight="bold"),
        text_color="#333333"
    )
    usage_title.pack(pady=(20, 10), padx=(200, 0))

    usage_text = """
1. Profile Management
   • Update your profile information using 'Edit Profile'
   • Change your password regularly for security
   • Upload a profile picture by clicking on the avatar

2. Financial Management
   • Track your income and expenses
   • Set budgets and financial goals
   • View financial reports and analytics

3. Security Tips
   • Use a strong password
   • Don't share your login credentials
   • Log out when using shared devices

4. Getting Help
   • Contact support for technical issues
   • Check FAQ section for common questions
   • Regular updates for new features
    """

    # Create a frame for the usage text to allow for proper left alignment
    usage_text_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    usage_text_frame.pack(fill=tk.X, pady=10, padx=20)
    
    usage_label = ctk.CTkLabel(
        usage_text_frame,
        text=usage_text,
        font=ctk.CTkFont(size=14),
        text_color="#666666",
        justify="left",
        anchor="w"
    )
    usage_label.pack(fill=tk.X, anchor="w")

    # Configure the scrolling
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    # Configure canvas size
    def configure_canvas(event):
        canvas.configure(width=event.width)
        
    canvas.bind("<Configure>", configure_canvas)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Privacy Policy & How to Use")
    root.geometry("900x600")
    
    create_privacy_page(root)
    
    root.mainloop()