import os
from cryptography.fernet import Fernet

# === Encryption Key Setup ===
KEY_FILE = "encryption.key"

if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as keyfile:
        keyfile.write(Fernet.generate_key())

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_message(message):
    cipher = Fernet(load_key())
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    cipher = Fernet(load_key())
    return cipher.decrypt(encrypted_message.encode()).decode()

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
