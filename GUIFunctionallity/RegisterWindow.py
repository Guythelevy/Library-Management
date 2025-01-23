import tkinter as tk
from tkinter import messagebox


class RegisterWindow:
    def __init__(self, parent, user_manager):

        self.user_manager = user_manager
        self.window = tk.Toplevel(parent)
        self.window.title("Register")
        self.window.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        # Username Entry
        tk.Label(self.window, text="Username:",font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        # Password Entry
        tk.Label(self.window, text="Password:",font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=5)

        # Register Button
        tk.Button(
            self.window,
            text="Register",
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
            command=self.submit_registration
        ).pack(pady=10)

    def submit_registration(self):
        """
        Handles user registration using UserManager.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return

        result = self.user_manager.register_user(username, password)
        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.window.destroy()
        else:
            messagebox.showerror("Error", result["message"])
