import tkinter as tk
from tkinter import messagebox
from security.encrypt import generate_2FA_secret
from database.passwordStorage import register_master_password, check_user_exists
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave, toggle_password

class RegisterNewUserPage(tk.TopLevel):
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
        self.password_entry = tk.Entry(self, show="*", font=fonts["text"])
        self.password_entry.pack()

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
            messagebox.showinfo(
                "2-Factor Authentication",
                f"2FA has been enabled for {username}.\nYour authentication key is: {totp_secret}\nPlease store this in a secure place."
            )
        else:
            register_master_password(username, password, enable_2FA=False)
        self.new_username = username  # Call the success callback with the username
        self.destroy()  # Close the registration window
