import base64
import hashlib
from nacl.secret import SecretBox

# Modes
REVERSE = "Reverter"
ENCRYPT = "Encriptar"

def expand_key(user_key):
    """Expand the user's key into 32 bytes via SHA-256."""
    return hashlib.sha256(user_key.encode()).digest()

def ft_encrypt(user_key, content):
    """Encrypt content using the given user_key."""
    key = expand_key(user_key)
    box = SecretBox(key)
    encrypted = box.encrypt(content)  # uses ChaCha20-Poly1305
    return encrypted

def ft_decrypt(user_key, encrypted):
    """Decrypt content using the given user_key."""
    key = expand_key(user_key)
    box = SecretBox(key)
    content = box.decrypt(encrypted)
    return content

def chacha20_poly1305(key, message, mode):
    """Encrypt or decrypt `message` using the provided `key` and `mode`."""
    if len(key) == 0:
        raise ValueError("Requires a non-empty key")
    
    if mode == REVERSE:
        # Decrypt
        decoded = base64.b64decode(message.encode())
        plaintext = ft_decrypt(key, decoded)
        return plaintext.decode()
    elif mode == ENCRYPT:
        # Encrypt
        ciphertext = ft_encrypt(key, message.encode())
        return base64.b64encode(ciphertext).decode()
    else:
        raise ValueError("Invalid mode")
