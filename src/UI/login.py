import tkinter as tk
from tkinter import messagebox
from database.passwordStorage import check_master_password
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts

def on_hover(e, button):
    button.config(bg=PRIMEARY_COLOR)

def on_leave(e, button):
    button.config(bg=SECONDARY_COLOR)


class LoginPage(tk.Frame):
    """Handles user login and registration."""
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success
        #self.parent.title("Login")
        fonts = get_fonts(parent)

        tk.Label(parent, text="Login", font=fonts["title"], bg=BACKGROUND_COLOR).pack(pady=(25,10), fill='x')

        tk.Label(parent, text="Username:", font=fonts["text"], bg=BACKGROUND_COLOR).pack(pady=(10,0))
        self.username_entry = tk.Entry(parent, font=fonts["text"])
        self.username_entry.pack()

        tk.Label(parent, text="Master Password:", font=fonts["text"], bg=BACKGROUND_COLOR).pack(pady=(10,0))
        self.password_entry = tk.Entry(parent, show="*", font=fonts["text"])
        self.password_entry.pack()

        self.login_button = tk.Button(parent, text="Login", font=fonts["button"], bg=SECONDARY_COLOR, command=self.login)
        self.login_button.pack(pady=(15,0))
        self.login_button.bind("<Enter>", lambda e: on_hover(e, self.login_button))
        self.login_button.bind("<Leave>", lambda e: on_leave(e, self.login_button))

        self.register_button = tk.Button(parent, text="Register", font=fonts["button"], bg=SECONDARY_COLOR, command=self.register)
        self.register_button.pack(pady=(15,0))
        self.register_button.bind("<Enter>", lambda e: on_hover(e, self.register_button))   
        self.register_button.bind("<Leave>", lambda e: on_leave(e, self.register_button))

    def login(self):
        """Checks the login credentials and switches to the dashboard if correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_master_password(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.on_success()  # Switch to the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        """Checks if user exists and registers if not."""

        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_master_password(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.on_success()
