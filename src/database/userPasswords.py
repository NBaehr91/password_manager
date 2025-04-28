import os
import json
from database.passwordStorage import USER_DB
from UI import appWindow
from security.encrypt import encode_password
import datetime

DATE_FORMAT = "%Y-%m-%d"


def sanitize_user(user):
    """Sanitizes the user input."""
    return "".join(c for c in user if c.isalnum() or c in (' ', '.', '_')).rstrip()

def open_passwords(user):
    """Opens the stored passwords for a user."""
    sanitized_user = sanitize_user(user)
    user_stored_pwd = sanitized_user + "_passwords.json"
    if not os.path.exists(user_stored_pwd):
        return {}

    try:
        with open(user_stored_pwd, "r") as f:
            user_passwords = json.load(f)
    except json.JSONDecodeError:
        return {}
    return user_passwords

def save_password(user, site, email, password):
    """
    Saves a new password for a user.

    Parameters:
    user (str): The username of the user.
    site (str): The site for which the password is being saved.
    email (str): The email associated with the site.
    password (str): The password to be saved.

    Returns:
    None
    """
    date_saved = datetime.datetime.now().strftime(DATE_FORMAT)
    sanitized_user = sanitize_user(user)
    user_stored_pwd = sanitized_user + "_passwords.json"
    if not os.path.exists(user_stored_pwd):
        with open(user_stored_pwd, "w") as f:
            json.dump({}, f)

    try:
        with open(user_stored_pwd, "r") as f:
            user_passwords = json.load(f)
    except json.JSONDecodeError:
        user_passwords = {}

    if site not in user_passwords:
        # If the site is not in the dictionary, add it
        user_passwords[site] = []
        user_passwords[site].append(
            {"email": email, 
             "password": password, 
             "date": date_saved}
             )
    else:
        # Check if the email already exists in the list for the site
        for entry in user_passwords[site]:
            if entry["email"] == email:
                # Update the existing entry
                entry["password"] = password
                break
        else:
            # If the email is not found, add a new entry
            user_passwords[site].append(
                {"email": email, 
                 "password": password, 
                 "date": date_saved}
                 )

    # Check if the content has changed before writing to the file
    try:
        with open(user_stored_pwd, "w") as f:
            json.dump(user_passwords, f, indent=4)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

