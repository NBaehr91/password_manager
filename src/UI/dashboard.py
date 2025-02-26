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
        self.key = password
        self.configure(bg=BACKGROUND_COLOR)
        self.root.geometry("800x500")
        #self.root.title("Dashboard")
        fonts = get_fonts(root)
        # Label and button
        self.password_label = tk.Label(self, text=f"{username}'s Passwords", font=fonts["title"], bg=BACKGROUND_COLOR)
        self.password_label.pack(pady=(25,10), fill='x')
        
        # Button to save password
        self.new_pw_button = tk.Button(self, text="New Password", font=fonts["button"], bg=SECONDARY_COLOR, command=self.save_new_passwords)
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
        new_password_window = NewPasswordPage(self.root, self.username, self.key)
        new_password_window.grab_set()

