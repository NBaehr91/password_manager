import tkinter as tk
from tkinter import messagebox
from database.passwordStorage import check_master_password

class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login")

        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Master Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        """Checks the login credentials and switches to the dashboard if correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_master_password(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.on_success()  # Switch to the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password.")
