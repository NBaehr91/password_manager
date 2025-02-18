import tkinter as tk
from tkinter import messagebox
from security.generatePassword import password_generator
from database.userPasswords import open_passwords, save_password
from UI.newPasswordSave import NewPasswordPage
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave

class Dashboard(tk.Frame):
    def __init__(self, root, username, password):
    
        super().__init__(root)
        self.root = root
        self.username = username
        self.configure(bg=BACKGROUND_COLOR)
        self.root.geometry("800x500")
        #self.root.title("Dashboard")
        fonts = get_fonts(root)
        # Label and button
        self.password_label = tk.Label(self, text=f"{username}'s Passwords", font=fonts["title"], bg=BACKGROUND_COLOR)
        self.password_label.pack(pady=(25,10), fill='x')
        
        # Button to save password
        self.new_pw_button = tk.Button(self, text="New Password", font=fonts["button"], bg=SECONDARY_COLOR, command=self.save_new_passwords, width=20, anchor="ne")
        self.new_pw_button.bind("<Enter>", lambda e: on_hover(e, self.new_pw_button))
        self.new_pw_button.bind("<Leave>", lambda e: on_leave(e, self.new_pw_button))
        self.new_pw_button.pack()

        # display sites saved in scrollable list
        self.password_list = open_passwords(username)
        self.password_listbox = tk.Listbox(self, width=50, height=15, font=fonts["list"], bg=BACKGROUND_COLOR, selectbackground=PRIMEARY_COLOR, selectforeground=TEXT_COLOR,)
        self.password_listbox.pack(pady=(10,0))
        for site in self.password_list:
            self.password_listbox.insert(tk.END, site)    

            

    # Popup window for new passwords
    def save_new_passwords(self):
        new_password_window = NewPasswordPage(self.root, self.username)
        new_password_window.grab_set()


        """new_password_window.title("New Password")
        new_password_window.geometry("300x500")
        
        # Labels and entries for site, email, and password
        tk.Label(new_password_window, text="Site or app name: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        site_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        site_entry.pack(fill='x', pady=(0,10))

        tk.Label(new_password_window, text="Email or Username: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        email_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        email_entry.pack(fill='x',pady=(0,10))

        tk.Label(new_password_window, text="Password: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        password_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        password_entry.pack(fill='x', pady=(0,10))

        self.save_button = tk.Button(new_password_window, text="Save", font=get_fonts(self.root)["button"], bg=SECONDARY_COLOR, command=self.save)
        self.save_button.pack(pady=(15,0))
        self.save_button.bind("<Enter>", lambda e: on_hover(e, self.save_button))
        self.save_button.bind("<Leave>", lambda e: on_leave(e, self.save_button))"""
"""
    def save(self):
        # Save the password to a file or database
        site = self.site_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if site and email and password:
            save_password(site, email, password)
            messagebox.showinfo("Success", "Password saved successfully!")
            self.site_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.new_password_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

        def generate_password(self):
        Generate a new secure password and display it.

        new_password = password_generator()
        self.password_display.config(state="normal")
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, new_password)
        self.password_display.config(state="readonly")
"""