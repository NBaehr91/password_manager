import json
import os
from security.encrypt import hash_master_password

USER_DB = "users.json"

def check_master_password(username, password):
    """Verifies if the username and hashed master password match stored data."""
    if not os.path.exists(USER_DB):
        return False  # No users exist yet
    
    create_user_password_file(username)  # Ensure the password file is created
    users = {}
    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        return False

    user_data = users.get(username)
    if not user_data:
        return False
    
    # Hash the provided password and compare it with the stored hash
    hashed_password = hash_master_password(password)

    # Checks if user is stored using previous format (string) or new format (dict)
    # if on previous format gives user a prompt to update to new format by asking to enable 2FA
    if isinstance(user_data, str):
        if user_data != hashed_password:
            return False
        return {"status": "update_user_2FA"}
    if isinstance(user_data, dict):
        if user_data.get("password") != hashed_password:
            return False

        if user_data.get("2FA_enabled"):
            return {
                "status": "2FA_needed", 
                "totp_secret": user_data.get("totp_secret")
                }
        return {"status": "success"}
    return False  # Invalid user data format


def register_master_password(username, password, totp_secret=None, enable_2FA=False):
    """Stores a new master password (hashed) for a user."""
    users = {}

    create_user_password_file(username)  # Ensure the password file is created

    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            pass

    users[username] = {
        "password": hash_master_password(password),
        "totp_secret": totp_secret if enable_2FA else None,
        "2FA_enabled": enable_2FA
    }

    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def check_user_exists(username):
    """Checks if a user already exists."""
    if not os.path.exists(USER_DB):
        return False

    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        return False

    return True if username in users else False

def create_user_password_file(username):
    """Creates a new password file for a user."""
    sanitized_user = "".join(c for c in username if c.isalnum() or c in (' ', '.', '_')).rstrip()
    USER_STORED_PWD = sanitized_user + "_passwords.json"
    if not os.path.exists(USER_STORED_PWD):
        with open(USER_STORED_PWD, "w") as f:
            json.dump({}, f)

def update_user_wth_2FA(username, secret_2FA_code):
    """Updates a user to enable 2FA."""
    users = {}

    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            pass

    user_data = users[username]
    if isinstance(user_data, str):
        # If the user only has a password, convert it to a dict with 2FA secret
        user_data = {"password": user_data,
                     "totp_secret": secret_2FA_code,
                     "2FA_enabled": True}
    else:
        users[username] = {
            "password": user_data["password"],
            "totp_secret": secret_2FA_code,
            "2FA_enabled": True
        }

    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

def update_user_wthout_2FA(username):
    """Updates a user to disable 2FA."""
    users = {}

    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            pass

    user_data = users[username]
    if isinstance(user_data, str):
        # If the user only has a password, convert it to a dict without 2FA
        user_data = {"password": user_data,
                     "2FA_enabled": False}
    else:
        users[username] = {
            "password": user_data["password"],
            "2FA_enabled": False
        }

    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)