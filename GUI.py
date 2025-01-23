from Managment import UserManager, LibraryManager
import tkinter as tk
from tkinter import messagebox
import logging

from GUIFunctionallity.AddBookWindow import AddBookWindow
from GUIFunctionallity.LendBookWindow import LendBookWindow
from GUIFunctionallity.LoginWindow import LoginWindow
from GUIFunctionallity.RegisterWindow import RegisterWindow
from GUIFunctionallity.RemoveBookWindow import RemoveBookWindow
from GUIFunctionallity.ReturnBookWindow import ReturnBookWindow
from GUIFunctionallity.ViewBooksWindow import ViewBooksWindow
from GUIFunctionallity.PopularBookWindow import PopularBookWindow

# This is the class that unifies all of the project
# Its the main GUI with buttons to all of the existing functions
# Some buttons are locked behind a login requirment decorator, so make sure you register and log-in

class GUI:
    logging.basicConfig(
        filename="LibraryLog.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Library Management System started.")

    def __init__(self, root):
        self.root = root
        self.library_manager = LibraryManager.LibraryManager()
        self.user_manager = UserManager.UserManager()
        self.current_user = None
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Library Management System")
        self.root.geometry("850x450")

        # Logged-in status
        self.logged_in_label = tk.Label(
            self.root,
            text="Logged in as: Not logged in",
            font=("Ariel", 16, "bold"),
            bg="#007BFF",
            fg="white",
            relief="groove",
            padx=20,
            pady=10,
        )
        self.logged_in_label.pack(anchor="center", pady=10)

        self.add_widgets()

    def add_widgets(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Button configuration
        buttons = [
            ("Add Book", self.add_book),
            ("Remove Book", self.remove_book),
            ("View Books", self.view_books),
            ("Lend Books", self.lend_books),
            ("Return Books", self.return_books),
            ("Login", self.login),
            ("Logout", self.logout),
            ("Register", self.register),
            ("Popular Books", self.popular_books),
            ("View Notifications", self.view_notifications)

        ]

        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 3)
            tk.Button(
                button_frame,
                text=text,
                font=("Ariel", 14, "bold"),
                bg="#007BFF",
                fg="white",
                activebackground="#0056b3",
                activeforeground="white",
                relief="raised",
                bd=3,
                width=20,
                height=2,
                command=command,
            ).grid(row=row, column=col, padx=10, pady=10)

    # ----------- GUI FUNCTIONALITY -------------

    def login(self):
        def on_login_success(username):
            user = self.user_manager.get_user_by_username(username)
            if not user:
                messagebox.showerror("Error", f"User '{username}' not found!")
                return
            self.current_user = user
            notifications = user.get_Notifcations_num()
            self.logged_in_label.config(
                text=f"Logged in as: {username}, you have {notifications} new notifications"
            )
            logging.info(f"User '{username}' logged in with {notifications} notifications.")

        # Open the login window
        LoginWindow(self.root, self.user_manager, on_login_success)

    def register(self):

        RegisterWindow(self.root, self.user_manager)

    # Decarator for requiring a login
    def require_login(func):
        def wrapper(self, *args, **kwargs):
            if not self.current_user:
                messagebox.showerror("Error", "You must be logged in to perform this action!")
                return
            return func(self, *args, **kwargs)

        return wrapper

    @require_login
    def add_book(self):

        AddBookWindow(self.root, self.library_manager)

    @require_login
    def remove_book(self):

        RemoveBookWindow(self.root, self.library_manager)

    @require_login
    def lend_books(self):

        LendBookWindow(self.root, self.library_manager)

    @require_login
    def return_books(self):

        ReturnBookWindow(self.root, self.library_manager)

    def view_books(self):

        ViewBooksWindow(self.root, self.library_manager)

    def popular_books(self):

        PopularBookWindow(self.root, self.library_manager)

    @require_login
    def logout(self):

        self.current_user = None
        self.logged_in_label.config(text="Logged in as: Not logged in")
        messagebox.showinfo("Success", "Logged out successfully!")


    @require_login
    def view_notifications(self):
        notifications = self.current_user.Notifications
        if not notifications:
            messagebox.showinfo("Notifications", "You have no notifications!")
            return

        notification_text = "\n".join([f"- {note}" for note in notifications])
        messagebox.showinfo("Notifications", f"Your notifications:\n\n{notification_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

