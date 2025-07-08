
import tkinter as tk
from tkinter import messagebox
import hashlib
from pos.db.database import get_session
from pos.db.models import User

class LoginScreen:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login POS")
        self.session = get_session()
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = self.session.query(User).filter_by(username=username, password_hash=password_hash, is_active=True).first()
        if user:
            messagebox.showinfo("Berhasil", f"Login berhasil sebagai {user.role}")
            self.on_login_success(user)
        else:
            messagebox.showerror("Gagal", "Username atau password salah.")
