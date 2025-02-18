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
