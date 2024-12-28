import tkinter as tk
from tkinter import ttk
import base64
import hashlib
from nacl.secret import SecretBox

# Modes
REVERSE = "reverse"
ENCRYPT = "encrypt"

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

def main():
    def process():
        """Callback for the 'Process' button."""
        user_text = text_entry.get("1.0", tk.END).strip()
        user_key = key_entry.get().strip()
        selected_mode = mode_var.get()

        # Clear previous result
        result_text.delete("1.0", tk.END)

        try:
            result = chacha20_poly1305(user_key, user_text, selected_mode)
            result_text.insert(tk.END, result)
        except Exception as e:
            result_text.insert(tk.END, f"Error: {str(e)}")

    # Create main window
    root = tk.Tk()
    root.title("Simple Encrypt/Decrypt GUI")

    # --- Text Input ---
    tk.Label(root, text="Text:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    text_entry = tk.Text(root, width=50, height=5)
    text_entry.grid(row=0, column=1, padx=5, pady=5)

    # --- Key Input ---
    tk.Label(root, text="Key:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    key_entry = tk.Entry(root, width=50)
    key_entry.grid(row=1, column=1, padx=5, pady=5)

    # --- Mode Selection ---
    tk.Label(root, text="Mode:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    mode_var = tk.StringVar(value=ENCRYPT)  # default mode
    mode_menu = ttk.Combobox(root, textvariable=mode_var, values=[ENCRYPT, REVERSE])
    mode_menu.grid(row=2, column=1, padx=5, pady=5)

    # --- Process Button ---
    process_button = tk.Button(root, text="Process", command=process)
    process_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # --- Result Display ---
    tk.Label(root, text="Result:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    result_text = tk.Text(root, width=50, height=5)
    result_text.grid(row=4, column=1, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()