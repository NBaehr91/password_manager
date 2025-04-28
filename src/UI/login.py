import tkinter as tk
from tkinter import messagebox
from database.passwordStorage import check_master_password, check_user_exists, register_master_password, update_user_wth_2FA, update_user_wthout_2FA
from UI.styles import BACKGROUND_COLOR, TEXT_COLOR, PRIMEARY_COLOR, SECONDARY_COLOR, get_fonts, on_hover, on_leave
from security.encrypt import get_master_key, generate_2FA_secret, verify_totp_code
from UI.registerUser import RegisterNewUserPage


class LoginPage(tk.Frame):
    """Handles user login and registration."""
    def __init__(self, root, on_success):
        super().__init__(root)
        self.root = root
        self.on_success = on_success
        #self.root.title("Login")
        fonts = get_fonts(root)

        tk.Label(
            self, text="Login", 
            font=fonts["title"], 
            bg=BACKGROUND_COLOR
            ).pack(pady=(25,10), fill='x')

        tk.Label(
            self, 
            text="Username:", 
            font=fonts["text"], 
            bg=BACKGROUND_COLOR
            ).pack(pady=(10,0))
        self.username_entry = tk.Entry(self, font=fonts["text"])
        self.username_entry.pack()

        tk.Label(
            self, 
            text="Master Password:", 
            font=fonts["text"], 
            bg=BACKGROUND_COLOR).pack(pady=(10,0))
        self.password_entry = tk.Entry(self, show="*", font=fonts["text"])
        self.password_entry.pack()

        self.login_button = tk.Button(
            self, 
            text="Login", 
            font=fonts["button"], 
            bg=SECONDARY_COLOR, 
            command=self.login
            )
        self.login_button.pack(pady=(15,0))
        self.login_button.bind("<Enter>", lambda e: on_hover(e, self.login_button))
        self.login_button.bind("<Leave>", lambda e: on_leave(e, self.login_button))

        self.register_button = tk.Button(
            self, 
            text="Register", 
            font=fonts["button"], 
            bg=SECONDARY_COLOR, 
            command=self.register
            )
        self.register_button.pack(pady=(15,0))
        self.register_button.bind("<Enter>", lambda e: on_hover(e, self.register_button))   
        self.register_button.bind("<Leave>", lambda e: on_leave(e, self.register_button))

    def login(self):
        """Checks the login credentials and switches to the dashboard if correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        masterkey = get_master_key(password)
        check_result = check_master_password(username, password)

        if check_result == False:
            messagebox.showerror("Error", "Invalid username or password.")
            return
        
        match check_result["status"]:
            case "update_user_2FA":
                enable_2FA = self.ask_enable_2FA_popup()
                if enable_2FA:
                    # Here you would handle the enabling of 2FA
                    secret_2FA_code = generate_2FA_secret()
                    messagebox.showinfo(
                        "2Factor Authentication", 
                        f"2FA enabled. Your secret code is: {secret_2FA_code}\nPlease store it securely."
                        )
                    update_user_wth_2FA(username, secret_2FA_code)
                else:
                    update_user_wthout_2FA(username)
                self.on_success(username, masterkey)  # Switch to the dashboard

            case "2FA_needed":
                # Here you would handle the 2FA verification process
                totp_code = self.ask_totp_code()
                if not verify_totp_code(check_result["totp_secret"], totp_code):
                    messagebox.showerror("Error", "Invalid TOTP code.")
                    return
                messagebox.showinfo("Success", "2FA verified successfully!")
                self.on_success(username, masterkey)  # Switch to the dashboard

            case "success":
                # If the user is already registered and no 2FA is needed
                self.on_success(username, masterkey)  # Switch to the dashboard

        if check_master_password(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.on_success(username, masterkey)  # Switch to the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        """Checks if user exists and registers if not."""
       
        new_user_window = RegisterNewUserPage(self.root)
        self.wait_window(new_user_window)  # Wait for the registration window to close

        if hasattr(new_user_window, 'new_username') and new_user_window.new_username:
            username = new_user_window.new_username
            messagebox.showinfo("Success", "New User Created!")
            self.on_success(username)  # Switch to the dashboard

    def ask_enable_2FA_popup(self):
        """Asks the user if they want to enable 2FA."""
        def on_yes():
            nonlocal response
            response = True
            popup.destroy()
        def on_no():
            nonlocal response
            response = False
            popup.destroy()

        response = None
        popup = tk.Toplevel(self)
        popup.grab_set()  # Make the popup modal
        popup.configure(bg=BACKGROUND_COLOR)
        popup.geometry("300x200")
        popup.title("Enable 2FA")
        text = tk.Label(
            popup, 
            text="Do you want to enable 2FA additional security?", 
            font=get_fonts(self.root)["text"],
            wraplength=250,
            )
        text.pack(pady=10, fill='x', expand=True)
        tk.Button(
            popup, 
            text="Yes", 
            command=on_yes
            ).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(
            popup, 
            text="No", 
            command=on_no
            ).pack(side=tk.RIGHT, padx=20, pady=10)

        def update_text_wraplength(event):
            text.config(wraplength=event.width * 0.9)

        popup.bind("<Configure>", update_text_wraplength)  # Update wraplength on resize
        self.wait_window(popup)  # Wait for the popup to close
        return response
    
    def ask_totp_code(self):
        """Asks the user to enter their TOTP code."""
        def on_submit():
            nonlocal totp_code
            totp_code = totp_entry.get()
            popup.destroy()

        totp_code = None
        popup = tk.Toplevel(self)
        popup.title("Enter TOTP Code")
        tk.Label(
            popup, 
            text="Enter your TOTP code:", 
            font=get_fonts(self.root)["text"]
            ).pack(pady=10)
        totp_entry = tk.Entry(popup, font=get_fonts(self.root)["text"])
        totp_entry.pack(pady=5)
        tk.Button(popup, text="Submit", command=on_submit).pack(pady=10)
        popup.grab_set()
        self.wait_window(popup)
        return totp_code