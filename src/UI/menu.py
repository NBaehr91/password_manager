import tkinter as tk
from UI.styles import BACKGROUND_COLOR, get_fonts, on_hover, on_leave, toggle_password
from database.passwordStorage import hash_master_password, check_master_password, change_master_password
from database.userPasswords import open_passwords, save_password

def create_menubar(app_window):
    """Creates a menubar for the application."""
    menubar = tk.Menu(app_window)
    app_window.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=save_password)
    file_menu.add_separator()
    file_menu.add_command(label="Logout", command=app_window.show_login)
    file_menu.add_command(label="Exit", command=app_window.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Preferences", command=lambda: print("Preferences"))
    settings_menu.add_command(label="Change Password", command=lambda: print("Change Password"))
    settings_menu.add_separator()
    settings_menu.add_command(label="App Info", command=lambda: print("Info"))
    menubar.add_cascade(label="Settings", menu=settings_menu)

def change_master_password(root):
    """Changes the password for the current user."""
    new_password_window = tk.Toplevel(root)
    new_password_window.title("Change Master Password")
    new_password_window.geometry("300x200")
    new_password_window.configure(bg=BACKGROUND_COLOR)
    fonts = get_fonts(root)

    tk.Label(
        new_password_window, 
        text="Enter Master Password:", 
        font=fonts["text"], 
        bg=BACKGROUND_COLOR
        ).pack(pady=(10,0))
    password_frame = tk.Frame(new_password_window, bg=BACKGROUND_COLOR)
    password_frame.pack(fill='x', pady=(0,10))
    password_entry = tk.Entry(
        password_frame, 
        show="*", 
        font=fonts["text"]
        )
    password_entry.pack(side="left", fill="x", expand=True)
    show_password_button = tk.Button(
        password_frame,
        text="Show",
        font=fonts["text"],
        bg=BACKGROUND_COLOR,
        command=toggle_password(password_entry, show_password_button)
        )
    show_password_button.pack(side="right", padx=(5,0))
    tk.Label(
        new_password_window, 
        text="Enter New Password:", 
        font=fonts["text"], 
        bg=BACKGROUND_COLOR
        ).pack(pady=(10,0))
    new_password_frame = tk.Frame(new_password_window, bg=BACKGROUND_COLOR)
    new_password_frame.pack(fill='x', pady=(0,10))
    new_password_entry = tk.Entry(
        new_password_frame, 
        show="*", 
        font=fonts["text"]
        )
    new_password_entry.pack(side="left", fill="x", expand=True)
    show_new_password_button = tk.Button(
        new_password_frame,
        text="Show",
        font=fonts["text"],
        bg=BACKGROUND_COLOR,
        command=lambda: toggle_password(new_password_entry, show_new_password_button)
        )
    show_new_password_button.pack(side="right", padx=(5,0))
    tk.Button(
        new_password_window, 
        text="Change Password", 
        font=fonts["text"], 
        bg=BACKGROUND_COLOR, 
        command=button_press
        ).pack(pady=(10,0))
    new_password_window.protocol("WM_DELETE_WINDOW", lambda: new_password_window.destroy())

    def button_press(event):
        """Handles button press events."""
        if check_master_password(root.username, password_entry.get()):
            if new_password_entry.get() == password_entry.get():
                tk.messagebox.showerror("Error", "New password cannot be the same as the old password.")
            else:
                change_master_password(root.username, hash_master_password(new_password_entry.get()))
                tk.messagebox.showinfo("Success", "Password changed successfully.")
                new_password_window.destroy()
        else:
            tk.messagebox.showerror("Error", "Incorrect master password.")
    pass