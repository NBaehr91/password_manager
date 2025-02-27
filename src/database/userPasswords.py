import os
import json
from database.passwordStorage import USER_DB
from UI import appWindow
from security.encrypt import encode_password
import datetime


def open_passwords(user):
    """Opens the stored passwords for a user."""
    sanitized_user = "".join(c for c in user if c.isalnum() or c in (' ', '.', '_')).rstrip()
    USER_STORED_PWD = sanitized_user + "_passwords.json"
    if not os.path.exists(USER_STORED_PWD):
        return {}

    try:
        with open(USER_STORED_PWD, "r") as f:
            user_passwords = json.load(f)
    except json.JSONDecodeError:
        return {}

    return user_passwords

def save_password(user, site, email, password):
    """Saves a new password for a user."""
    sanitized_user = "".join(c for c in user if c.isalnum() or c in (' ', '.', '_')).rstrip()
    USER_STORED_PWD = sanitized_user + "_passwords.json"
    date_saved = datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(USER_STORED_PWD):
        with open(USER_STORED_PWD, "w") as f:
            json.dump({}, f)

    try:
        with open(USER_STORED_PWD, "r") as f:
            user_passwords = json.load(f)
    except json.JSONDecodeError:
        user_passwords = {}

    if site not in user_passwords:
        # If the site is not in the dictionary, add it
        user_passwords[site] = []
        user_passwords[site].append({"email": email, "password": password, "date": date_saved})
    elif email not in user_passwords[site]:
        # If the email is not in the list for the site, add it
        user_passwords[site].append({"email": email, "password": password, "date": date_saved})
    else:
        # If the site is already in the dictionary, update the email and password
        user_passwords[site]["email"] = email
        user_passwords[site]["password"] = password
        user_passwords[site]["date"] = date_saved

    with open(USER_STORED_PWD, "w") as f:
        json.dump(user_passwords, f, indent=4)



