import os
from cryptography.fernet import Fernet

# === Encryption Key Setup ===
KEY_FILE = "encryption.key"

def create_key_if_missing():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as keyfile:
            keyfile.write(key)
        print("✅ Encryption key created and saved.")
    else:
        print("🔒 Encryption key already exists, not creating a new one.")

def load_key():
    return open(KEY_FILE, "rb").read()

# Call this only once at server startup
create_key_if_missing()

def encrypt_message(message):
    cipher = Fernet(load_key())
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    cipher = Fernet(load_key())
    try:
        return cipher.decrypt(encrypted_message.encode()).decode()
    except Exception:
        return "❌ Cannot decrypt this message (corrupted or wrong key)"

# === Bandwidth Estimation ===
def calculate_bandwidth(message, file=None):
    size = len(message.encode()) / 1024  # in KB
    if file:
        size += file.size / 1024
    return round(size, 2)

# === Spam Filter ===
SPAM_WORDS = ["money", "lottery", "win", "prize", "free", "urgent"]

def is_spam(message):
    return any(word in message.lower() for word in SPAM_WORDS)
