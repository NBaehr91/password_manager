import tkinter as tk
from UI.login import LoginPage
from UI.dashboard import Dashboard
from UI.styles import BACKGROUND_COLOR
from UI.menu import create_menubar

class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.configure(bg=BACKGROUND_COLOR)
        
        # Start with login page
        self.show_login()

    def show_login(self):
        """Display login screen."""
        self.clear_window()
        LoginPage(self, self.on_successful_login).pack(fill='both', expand=True)

    def on_successful_login(self, username, key):
        """Callback function to switch to the dashboard after successful login."""
        self.user = username
        self.current_user_key = key
        self.show_dashboard()

    def show_dashboard(self):
        """Display the main dashboard after login."""
        self.clear_window()
        Dashboard(self).pack(fill='both', expand=True)

        create_menubar(self)

    def clear_window(self):
        """Clears the current window to load a new page."""
        for widget in self.winfo_children():
            widget.destroy()

    def run(self):
        """Runs the Tkinter main event loop."""
        # Runs the Tkinter main event loop, waiting for events and updating the UI
        self.mainloop()
