import tkinter as tk

def create_menubar(root):
    """Creates a menubar for the application."""
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: print("New File"))
    file_menu.add_separator()
    file_menu.add_command(label="Logout", command=root.show_login)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Preferences", command=lambda: print("Preferences"))
    settings_menu.add_command(label="Change Password", command=lambda: print("Change Password"))
    settings_menu.add_separator()
    settings_menu.add_command(label="App Info", command=lambda: print("Info"))
    menubar.add_cascade(label="Settings", menu=settings_menu)
