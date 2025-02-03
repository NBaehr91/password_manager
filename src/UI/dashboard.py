import tkinter as tk
from security.generatePassword import password_generator
from database.userPasswords import open_passwords, save_password
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts

def on_hover(e, button):
    button.config(bg=PRIMEARY_COLOR)

def on_leave(e, button):
    button.config(bg=SECONDARY_COLOR)

class Dashboard(tk.Frame):
    def __init__(self, root, username):
    
        super().__init__(root)
        self.root = root
        self.username = username
        self.root.geometry("800x600")
        #self.root.title("Dashboard")
        fonts = get_fonts(root)
        # Label and button
        self.password_label = tk.Label(self, text=f"{username}'s Passwords", font=fonts["title"], bg=BACKGROUND_COLOR)
        self.password_label.pack(pady=(25,10), fill='x')
        
        self.password_display = tk.Entry(self, state="readonly", width=30)
        self.password_display.pack()
        
        # Button to save password
        self.new_pw_button = tk.Button(self, text="New Password", font=fonts["button"], bg=SECONDARY_COLOR, command=self.save_new_passwords)
        self.new_pw_button.bind("<Enter>", lambda e: on_hover(e, self.new_pw_button))
        self.new_pw_button.bind("<Leave>", lambda e: on_leave(e, self.new_pw_button))
        self.new_pw_button.pack()

    def save_new_passwords(self):
       # Popup window for new passwords
        new_password_window = tk.Toplevel(self.root)
        new_password_window.title("New Password")
        new_password_window.geometry("300x500")
        
        # Placeholder for saved passwords
        tk.Label(new_password_window, text="Site or app name: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        site_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        site_entry.pack(fill='x', pady=(0,10))
        tk.Label(new_password_window, text="Email: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        email_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        email_entry.pack(fill='x',pady=(0,10))
        tk.Label(new_password_window, text="Password: ", font=get_fonts(self.root)["text"], bg=BACKGROUND_COLOR, anchor="w").pack(fill='x')
        password_entry = tk.Entry(new_password_window, font=get_fonts(self.root)["text"])
        password_entry.pack(fill='x', pady=(0,10))
        tk.Button(new_password_window, text="Save", font=get_fonts(self.root)["button"], bg=SECONDARY_COLOR, command=lambda: save_password(site_entry, email_entry, password_entry)).pack(pady=(15,0))

    """def generate_password(self):
        Generate a new secure password and display it.

        new_password = password_generator()
        self.password_display.config(state="normal")
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, new_password)
        self.password_display.config(state="readonly")
"""