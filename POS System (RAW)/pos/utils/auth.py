# utils/auth.py
import hashlib
import sqlite3
from db.models import DB_PATH

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, role, is_active FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        stored_hash, role, is_active = row
        if is_active and stored_hash == hash_password(password):
            return role  # Return role if verified
    return None