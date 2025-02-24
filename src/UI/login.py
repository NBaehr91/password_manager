import tkinter as tk
from tkinter import messagebox
from database.passwordStorage import check_master_password, check_user_exists, register_master_password
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave
from security.encrypt import get_master_key

class LoginPage(tk.Frame):
    """Handles user login and registration."""
    def __init__(self, root, on_success):
        super().__init__(root)
        self.root = root
        self.on_success = on_success
        #self.root.title("Login")
        fonts = get_fonts(root)

        tk.Label(self, text="Login", font=fonts["title"], bg=BACKGROUND_COLOR).pack(pady=(25,10), fill='x')

        tk.Label(self, text="Username:", font=fonts["text"], bg=BACKGROUND_COLOR).pack(pady=(10,0))
        self.username_entry = tk.Entry(self, font=fonts["text"])
        self.username_entry.pack()

        tk.Label(self, text="Master Password:", font=fonts["text"], bg=BACKGROUND_COLOR).pack(pady=(10,0))
        self.password_entry = tk.Entry(self, show="*", font=fonts["text"])
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", font=fonts["button"], bg=SECONDARY_COLOR, command=self.login)
        self.login_button.pack(pady=(15,0))
        self.login_button.bind("<Enter>", lambda e: on_hover(e, self.login_button))
        self.login_button.bind("<Leave>", lambda e: on_leave(e, self.login_button))

        self.register_button = tk.Button(self, text="Register", font=fonts["button"], bg=SECONDARY_COLOR, command=self.register)
        self.register_button.pack(pady=(15,0))
        self.register_button.bind("<Enter>", lambda e: on_hover(e, self.register_button))   
        self.register_button.bind("<Leave>", lambda e: on_leave(e, self.register_button))

    def login(self):
        """Checks the login credentials and switches to the dashboard if correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        masterkey = get_master_key(password)
        if check_master_password(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.on_success(username, masterkey)  # Switch to the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        """Checks if user exists and registers if not."""
       
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not check_user_exists(username):
            register_master_password(username, password)
            messagebox.showinfo("Success", "New User Created!")
            self.on_success(username)  # Switch to the dashboard

        else:
            messagebox.showerror("Error", "User already exists.")
