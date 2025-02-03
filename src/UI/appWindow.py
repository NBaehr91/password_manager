import tkinter as tk
from UI.login import LoginPage
from UI.dashboard import Dashboard
from UI.styles import BACKGROUND_COLOR

class AppWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Start with login page
        self.show_login()

    def show_login(self):
        """Display login screen."""
        self.clear_window()
        self.login_page = LoginPage(self.root, self.on_successful_login)
        self.login_page.pack(fill='both', expand=True)

    def on_successful_login(self, username):
        """Callback function to switch to the dashboard after successful login."""
        self.current_user = username
        self.show_dashboard()

    def show_dashboard(self):
        """Display the main dashboard after login."""
        self.clear_window()
        self.dashboard = Dashboard(self.root, self.current_user)
        self.dashboard.pack(fill='both', expand=True)

    def clear_window(self):
        """Clears the current window to load a new page."""
        for widget in self.root.winfo_children():
            widget.destroy()
            widget.pack_forget()

    def run(self):
        """Runs the Tkinter main event loop."""
        # Runs the Tkinter main event loop, waiting for events and updating the UI
        self.root.mainloop()
