import json
import os
from security.encrypt import hash_master_password

USER_DB = "users.json"

def check_master_password(username, password):
    """Verifies if the username and hashed master password match stored data."""
    if not os.path.exists(USER_DB):
        return False  # No users exist yet

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
    if os.path.exists(USER_DB):
        try:
            with open(USER_DB, "r") as f:
                users = json.load(f)
        except json.JSONDecodeError:
            pass

    users[username] = hash_master_password(password)

    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)
