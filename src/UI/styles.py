from tkinter import font

PRIMEARY_COLOR = "#2E3A4F"
SECONDARY_COLOR = "#F0F3F5"
BACKGROUND_COLOR = "#F0F3F5"
TEXT_COLOR = "#2E3A4F"
FONT = "Century Schoolbook"

def get_fonts(root):
    return{
        "title": font.Font(root, family=FONT, size=18, weight="bold"),
        "subtitle": font.Font(root, family=FONT, size=14),
        "text": font.Font(root, family=FONT, size=12),
        "button": font.Font(root, family=FONT, size=12),
        "list": font.Font(root, family=FONT, size=14,),
    }
    
def on_hover(e, button):
    button.config(bg=PRIMEARY_COLOR)

def on_leave(e, button):    
    button.config(bg=SECONDARY_COLOR)

def toggle_password(password_entry, show_button, password_visible):
    """
    Toggles the visibility of the password in the password entry field.
    
    If the password is currently visible, it hides it by setting the show attribute to "*".
    If the password is currently hidden, it shows it by setting the show attribute to an empty string.
    """
    if password_visible:
        password_entry.config(show="*")
        show_button.config(text="Show")
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")
    return not password_visible
