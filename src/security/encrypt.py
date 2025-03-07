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

def encode_password(password, masterkey, numpasses):
    """Encodes a password using the master key and number of passes."""

    char_blocks = [ord(c) for c in password]
    encrypted_blocks = []
    passkeys = generate_encryption_key(masterkey, numpasses)

    # Split each character into two 4-bit blocks
    for block in char_blocks:
        left = block >> 4
        right = block & 0xF

        # Perform the encoding rounds
        for i in range(numpasses):
            new_left = right
            new_right = left ^ encode_rounds(right, passkeys[i])
            left = new_left
            right = new_right
        
        # Combine the blocks back into a single byte
        encrypted_block = (left << 4) | right
        # Append the encrypted block to the list
        encrypted_blocks.append(encrypted_block)
    
    # Convert the encrypted blocks back to a string
    encrypted_password = ''.join(chr(block) for block in encrypted_blocks)
    xor_key = masterkey & 0xFF
    encrypted_password = xor_encrypt_decrypt(encrypted_password, xor_key)
    return encrypted_password

def decode_password_blocks(encrypted_block_pairs, masterkey, numpasses):
    """Decodes the encrypted password blocks using the master key and number of passes."""
    left, right = encrypted_block_pairs
    passkeys = generate_encryption_key(masterkey, numpasses)[::-1]  # Reverse the passkeys for decryption
    # Perform the decoding rounds
    for i in range(numpasses):
        new_right = left
        new_left = right ^ encode_rounds(left, passkeys[i])
        left = new_left
        right = new_right

    return chr(left) + chr(right)

def decode_password(encrypted_password_blocks, masterkey, numpasses):
    """Decodes an encrypted password using the master key and number of passes."""
    xor_key = masterkey & 0xFF
    encrypted_password = xor_encrypt_decrypt(encrypted_password_blocks, xor_key)
    decrypted_password = ""

    for i in range(0, len(encrypted_password), 2):
        encrypted_pairs = (ord(encrypted_password[i]), ord(encrypted_password[i+1]))
        decrypted_password += decode_password_blocks(encrypted_pairs, masterkey, numpasses)

    return decrypted_password
    
def xor_encrypt_decrypt(data, key):
    """Encrypts or decrypts data using XOR with the given key."""
    return ''.join(chr(ord(c) ^ key) for c in data)