import hashlib

def hash_master_password(password: str) -> str:
    
    encoded_password = password.encode()
    hashed_password = hashlib.sha256(encoded_password)
    return hashed_password.hexdigest()

# generates password masterkey from user's master password
def get_master_key(password):
    hashed_password = hash_master_password(password)
    password_key = int(hashed_password, 16) % 0xFFFF
    return password_key

# generates a list of subkeys from the master key to encrypt/decrypt saved passwords
def generate_encryption_key(masterkey, numpasses):
    
    passkeys = []
    for i in range(numpasses):
        subkey = (masterkey >> i) ^ (masterkey << (i%4)) & 0xFFFF
        passkeys.append(subkey)

    return passkeys
  
def encode_rounds(val, subkey):
    val = (val ^ subkey)
    val = ((val << 2) | (val >> 4)) & 0xFF
    val = (val ^ (subkey>>2))
    return val