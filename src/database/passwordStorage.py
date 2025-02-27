import json
import os
from security.encrypt import hash_master_password

USER_DB = "users.json"

def check_master_password(username, password):
    """Verifies if the username and hashed master password match stored data."""
    if not os.path.exists(USER_DB):
        return False  # No users exist yet
    
    create_user_password_file(username)  # Ensure the password file is created

    try:
        with open(USER_DB, "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        return False

    
    hashed_password = hash_master_password(password)
    return users.get(username) == hashed_password

def register_master_password(username, password):
    """Stores a new master password (hashed) for a user."""
    users = {}

    create_user_password_file(username)  # Ensure the password file is created

    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            pass

    users[username] = hash_master_password(password)

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
