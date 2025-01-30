import tkinter as tk
from security.generatePassword import password_generator

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        
        # Label and button
        self.password_label = tk.Label(root, text="Generated Password:")
        self.password_label.pack()
        
        self.password_display = tk.Entry(root, state="readonly", width=30)
        self.password_display.pack()
        
        self.generate_button = tk.Button(root, text="Generate New Password", command=self.generate_password)
        self.generate_button.pack()

    def generate_password(self):
        """Generate a new secure password and display it."""
        new_password = password_generator()
        self.password_display.config(state="normal")
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, new_password)
        self.password_display.config(state="readonly")
