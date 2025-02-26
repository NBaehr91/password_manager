import tkinter as tk
from tkinter import messagebox
from security.generatePassword import password_generator
from security.encrypt import encode_password, decode_password
from database.userPasswords import open_passwords, save_password
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave

class NewPasswordPage(tk.Toplevel):
    def __init__(self, root, username, site, key):
        super().__init__(root)
        passwords = open_passwords(username)
        show_password = decode_password(passwords[site]["password"], key, 10)
        self.username = username
        self.key = key
        self.configure(bg=BACKGROUND_COLOR)
        self.geometry("300x500")
        fonts = get_fonts(root)
        
        # Labels and entries for site, email, and password
        tk.Label(self, text="Site or app name: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.site_entry = tk.Entry(self, font=fonts["text"])
        self.site_entry.insert(0, site)
        self.site_entry.config(state="readonly")
        self.site_entry.pack(fill='x', pady=(0,10))

        tk.Label(self, text="Email or Username: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.email_entry = tk.Entry(self, font=fonts["text"])
        self.email_entry.insert(0, passwords[site]["email"])
        self.email_entry.config(state="readonly")
        self.email_entry.pack(fill='x',pady=(0,10))

        tk.Label(self, text="Password: ", font=fonts["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        self.password_entry = tk.Entry(self, font=fonts["text"])
        self.password_entry.insert(0, show_password)
        self.password_entry.config(state="readonly")
        #toggle password visibility
        self.password_entry.bind("<Button-1>", lambda e: self.password_entry.config(show=""))
        self.password_entry.bind("<ButtonRelease-1>", lambda e: self.password_entry.config(show="*"))
        self.password_entry.pack(fill='x', pady=(0,10))

        self.edit_button = tk.Button(self, text="Edit", font=fonts["button"], bg=SECONDARY_COLOR, command=self.edit)
        self.edit_button.pack(pady=(15,0))
        self.edit_button.bind("<Enter>", lambda e: on_hover(e, self.edit_button))
        self.edit_button.bind("<Leave>", lambda e: on_leave(e, self.edit_button))

        self.save_button = tk.Button(self, text="Save", font=fonts["button"], bg=SECONDARY_COLOR, command=self.save)
        self.save_button.pack(pady=(15,0))
        self.save_button.bind("<Enter>", lambda e: on_hover(e, self.save_button))
        self.save_button.bind("<Leave>", lambda e: on_leave(e, self.save_button))

    def edit(self):
        self.site_entry.config(state="normal")
        self.email_entry.config(state="normal")
        self.password_entry.config(state="normal")
        self.site_entry.focus_set()
        self.edit_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.edit_button.config(text="Editing...")

    def save(self):
        # Save the password to a file or database
        site = self.site_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        #warn user password will be overwritten
        if messagebox.askyesno("Warning", "Are you sure you want to overwrite this password?"):
            pass
        else:
            return

        if site and email and password:
            encrpt_password = encode_password(password, self.key, 10)
            save_password(self.username, site, email, encrpt_password)
            messagebox.showinfo("Success", "Password saved successfully!")
            self.site_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")