import tkinter as tk
from UI.login import LoginPage
from UI.dashboard import Dashboard

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        
        # Start with login page
        self.show_login()

    def show_login(self):
        """Display login screen."""
        self.clear_window()
        self.login_page = LoginPage(self.root, self.show_dashboard)

    def show_dashboard(self):
        """Display the main dashboard after login."""
        self.clear_window()
        self.dashboard = Dashboard(self.root)

    def clear_window(self):
        """Clears the current window to load a new page."""
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def run(self):
        """Runs the Tkinter main event loop."""
        # Runs the Tkinter main event loop, waiting for events and updating the UI
        self.root.mainloop()
