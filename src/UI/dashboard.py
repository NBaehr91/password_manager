import tkinter as tk
from tkinter import messagebox, ttk
from security.generatePassword import password_generator
from database.userPasswords import open_passwords, save_password
from UI.newPasswordSave import NewPasswordPage
from UI.showPassword import PasswordPage
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave
from UI.menu import create_menubar

class Dashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.username = self.master.user
        self.key = self.master.current_user_key
        self.configure(bg=BACKGROUND_COLOR)
        self.master.geometry("800x500")
        #self.root.title("Dashboard")
        fonts = get_fonts(self.master)

        # Label and button
        self.password_label = tk.Label(
            self, 
            text=f"{self.username}'s Passwords", 
            font=fonts["title"], 
            bg=BACKGROUND_COLOR
            )
        self.password_label.pack(pady=(25,10), fill='x')
        
        # Button to save password
        self.new_pw_button = tk.Button(
            self, 
            text="New Password", 
            font=fonts["button"], 
            bg=SECONDARY_COLOR, 
            command=self.save_new_passwords
            )
        self.new_pw_button.bind("<Enter>", lambda e: on_hover(e, self.new_pw_button))
        self.new_pw_button.bind("<Leave>", lambda e: on_leave(e, self.new_pw_button))
        self.new_pw_button.pack()

        # display sites saved in scrollable list
        self.password_dict = open_passwords(self.username)
        self.password_list = list(self.password_dict.keys())
        self.password_list_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        self.password_list_frame.pack(pady=(10,0), fill='x')
        self.password_list_frame.grid_rowconfigure(0, weight=1)

        self.password_listbox = ttk.Treeview(
            self.password_list_frame, 
            columns=("site", "date"), 
            show="headings", 
            height=10
            )
        self.password_listbox.heading("site", text="Site or App")
        self.password_listbox.heading("date", text="Date Saved")
        self.password_listbox.column("site", width=300)
        self.password_listbox.column("date", width=100)
        self.password_listbox.pack(pady=(10,0), fill='x')
        
        for site in self.password_list:
            self.password_listbox.insert(
                "", 
                tk.END, 
                values=(site, self.password_dict[site][0]["date"])
                )
        # Bind the listbox selection to the show_password method
        self.password_listbox.bind("<<TreeviewSelect>>", self.show_password)

    # Popup window for new passwords
    def save_new_passwords(self):
        new_password_window = NewPasswordPage(self.master, self.username, self.key)
        new_password_window.grab_set()
        new_password_window.focus_set()
        # Wait for the new password window to close
        self.wait_window(new_password_window)  
        # # After the new password window is closed, update the listbox
        self.update_listbox()

    def update_listbox(self):
        """
        Update the listbox with the new password.
        
        This method is called when a new password is saved. 
        It updates the listbox with the new password.
        """
        self.password_dict = open_passwords(self.username)
        self.password_list = list(self.password_dict.keys())
        self.password_listbox.delete(*self.password_listbox.get_children())
        for site in self.password_list:
            self.password_listbox.insert(
                "", 
                tk.END, 
                values=(site, self.password_dict[site][0]["date"])
                )

    def show_password(self, event):
        """
        Display the password for the selected site in a new window.
        
        This method is triggered when a site is selected from the listbox.
        It opens a new window displaying the password for the selected site.
        """
        selected_item = self.password_listbox.selection()[0]
        selected_site = self.password_listbox.item(selected_item, "values")[0]
        if selected_site:
            new_password_window = PasswordPage(
                self.master, 
                self.username, 
                selected_site, 
                self.key
                )
            new_password_window.grab_set()
            new_password_window.focus_set()
