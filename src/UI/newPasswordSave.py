import tkinter as tk
from tkinter import messagebox
from security.generatePassword import password_generator
from database.userPasswords import open_passwords, save_password
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave

class NewPasswordPage(tk.Toplevel):
    def __init__(self, root, username):
        super().__init__(root)
        self.username = username
        self.configure(bg=BACKGROUND_COLOR)
        self.geometry("300x500")
        fonts = get_fonts(root)
        
        # Labels and entries for site, email, and password
        tk.Label(self, text="Site or app name: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.site_entry = tk.Entry(self, font=fonts["text"])
        self.site_entry.pack(fill='x', pady=(0,10))

        tk.Label(self, text="Email or Username: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.email_entry = tk.Entry(self, font=fonts["text"])
        self.email_entry.pack(fill='x',pady=(0,10))

        tk.Label(self, text="Password: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.password_entry = tk.Entry(self, font=fonts["text"])
        self.password_entry.pack(fill='x', pady=(0,10))

        self.save_button = tk.Button(self, text="Save", font=fonts["button"], bg=SECONDARY_COLOR, command=self.save)
        self.save_button.pack(pady=(15,0))
        self.save_button.bind("<Enter>", lambda e: on_hover(e, self.save_button))
        self.save_button.bind("<Leave>", lambda e: on_leave(e, self.save_button))

    def save(self):
        # Save the password to a file or database
        site = self.site_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if site and email and password:
            save_password(self.username, site, email, password)
            messagebox.showinfo("Success", "Password saved successfully!")
            self.site_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")