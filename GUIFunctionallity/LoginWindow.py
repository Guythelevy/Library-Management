import tkinter as tk
from tkinter import messagebox


class LoginWindow:
    def __init__(self, parent, user_manager, on_login_success):

        self.user_manager = user_manager
        self.on_login_success = on_login_success
        self.window = tk.Toplevel(parent)
        self.window.title("Login")
        self.window.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        # Username Entry
        tk.Label(self.window, text="Username:",  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Password Entry
        tk.Label(self.window, text="Password:",  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        tk.Button(
            self.window,
            text="Login",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.validate_login
        ).pack(pady=10)

    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        result = self.user_manager.validate_login(username, password)
        if result["success"]:
            self.on_login_success(username)
            self.window.destroy()
        else:
            messagebox.showerror("Error", result["message"])
