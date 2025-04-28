import tkinter as tk
from tkinter import messagebox
from security.encrypt import generate_2FA_secret
from database.passwordStorage import register_master_password, check_user_exists
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave, toggle_password
import qrcode
from PIL import ImageTk

class RegisterNewUserPage(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.configure(bg=BACKGROUND_COLOR)
        self.geometry("300x500")
        fonts = get_fonts(root)

        tk.Label(
            self, 
            text="Register New User", 
            font=fonts["title"], 
            bg=BACKGROUND_COLOR
            ).pack(pady=(25,10), fill='x')

        tk.Label(
            self, 
            text="Username:", 
            font=fonts["text"], 
            bg=BACKGROUND_COLOR
            ).pack(pady=(10,0))
        self.username_entry = tk.Entry(self, font=fonts["text"])
        self.username_entry.pack()

        tk.Label(
            self, 
            text="Master Password:", 
            font=fonts["text"], 
            bg=BACKGROUND_COLOR
            ).pack(pady=(10,0))
        self.password_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.password_frame.pack(fill='x', pady=(0,10))
        self.password_entry = tk.Entry(
            self.password_frame, 
            show="*", 
            font=fonts["text"]
            )
        self.password_entry.pack(side="left", fill="x", expand=True)
        self.show_password_button = tk.Button(
            self.password_frame,
            text="Show",
            font=fonts["text"],
            bg=BACKGROUND_COLOR,
            command=self.toggle_password_visibility
            )
        self.show_password_button.pack(side="right", padx=(5,0))

        self.enable_2FA_var = tk.BooleanVar(value=False)
        enable_2FA = tk.Checkbutton(
            self, 
            text="Enable 2-Factor Authentication", 
            font=fonts["text"], 
            bg=BACKGROUND_COLOR, 
            variable=self.enable_2FA_var
            )
        enable_2FA.pack(pady=(10,0))

        self.register_button = tk.Button(
            self, 
            text="Register", 
            font=fonts["button"], 
            bg=SECONDARY_COLOR, 
            command=self.register
            )
        self.register_button.pack(pady=(15,0))
        self.register_button.bind("<Enter>", lambda e: on_hover(e, self.register_button))
        self.register_button.bind("<Leave>", lambda e: on_leave(e, self.register_button))

    def register(self):
        """Registers a new user with a master password."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        enable_2FA = self.enable_2FA_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if check_user_exists(username):
            messagebox.showerror("Error", "Username already exists.")
            return
        
        if enable_2FA:
            # Here you would generate a TOTP secret code
            totp_secret = generate_2FA_secret()
            register_master_password(username, password, totp_secret, enable_2FA=True)
            self.show_qr_code(totp_secret)  # Show the QR code for the user to scan
        else:
            register_master_password(username, password, enable_2FA=False)
        self.new_username = username  # Call the success callback with the username
        self.new_key = password  # Call the success callback with the key
        self.destroy()  # Close the registration window

    def show_qr_code(self, secret):
        """Displays a QR code for the 2FA secret."""
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(secret)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img = img.resize((200,200))
        qr_img = ImageTk.PhotoImage(img)

        popup_qr = tk.Toplevel(self)
        popup_qr.title("Scan QR Code")
        popup_qr.geometry("300x300")
        popup_qr.configure(bg=BACKGROUND_COLOR)

        tk.Label(
            popup_qr, 
            text="Scan this QR code with your 2FA app:", 
            bg=BACKGROUND_COLOR, 
            font=get_fonts(self)["text"]
            ).pack(pady=(10, 0))

        tk.Label(popup_qr, image=qr_img, bg=BACKGROUND_COLOR).pack(pady=(10, 0))

        popup_qr.qr_img = qr_img  # Keep a reference to avoid garbage collection
        tk.Button(
            popup_qr, 
            text="Close", 
            command=popup_qr.destroy, 
            bg=SECONDARY_COLOR, 
            font=get_fonts(self)["button"]
            ).pack(pady=(10, 0))
        
        self.wait_window(popup_qr)  # Wait for the QR code window to close before continuing
    
    def toggle_password_visibility(self):
        """Toggles the visibility of the password entry field."""
        self.password_visible = toggle_password(
            self.password_entry, 
            self.show_password_button, 
            self.password_visible
        )