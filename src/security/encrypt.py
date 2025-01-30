import hashlib
"""
    Parameters:
    password (str): The master password to be hashed.

    Returns:
    str: The hashed password as a hexadecimal string.
"""
def hash_master_password(password: str) -> str:
    
    encoded_password = password.encode()
    hashed_password = hashlib.sha256(encoded_password)
    return hashed_password.hexdigest()

def encode_password(password: str) -> str:
    """Encodes the given password string."""
    return password.encode()
  
