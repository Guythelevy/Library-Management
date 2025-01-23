import tkinter as tk
from tkinter import messagebox
import logging

class LendBookWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.available_books = self.library_manager.list_available_books()  # Fetch available books
        self.unavailable_books = self.library_manager.list_unavailable_books()  # Fetch unavailable books
        self.window = tk.Toplevel(parent)
        self.window.title("Lend Book")
        self.window.geometry("700x600")
        self.create_widgets()

    def create_widgets(self):
        # Lender Details
        lender_frame = tk.Frame(self.window)
        lender_frame.pack(pady=5, fill=tk.X)

        tk.Label(lender_frame, text="Lender Name:", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        self.lender_name_entry = tk.Entry(lender_frame)
        self.lender_name_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Label(lender_frame, text="Lender Phone Number:", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        self.lender_phone_entry = tk.Entry(lender_frame)
        self.lender_phone_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Available Books List
        tk.Label(self.window, text="Available Books to Lend:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.available_tree = tk.Listbox(self.window, height=8)
        self.available_tree.pack(fill=tk.BOTH, expand=False, pady=10)

        try:
            for book in self.available_books:
                self.available_tree.insert(tk.END, f"{book.name} by {book.author} - Copies: {book.copies}")
            logging.info("Displayed available books successfully")
        except Exception as e:
            logging.info("Displayed available books fail")

        tk.Button(
            self.window, text="Lend Book", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
            command=self.lend_selected_book
        ).pack(pady=10)

        # Requester Details
        requester_frame = tk.Frame(self.window)
        requester_frame.pack(pady=5, fill=tk.X)

        tk.Label(requester_frame, text="Requester Name:", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        self.requester_name_entry = tk.Entry(requester_frame)
        self.requester_name_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        tk.Label(requester_frame, text="Requester Phone Number:", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        self.requester_phone_entry = tk.Entry(requester_frame)
        self.requester_phone_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Unavailable Books List
        tk.Label(self.window, text="Unavailable Books to Request:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.unavailable_tree = tk.Listbox(self.window, height=8)
        self.unavailable_tree.pack(fill=tk.BOTH, expand=False, pady=10)

        for book in self.unavailable_books:
            observers = ", ".join(str(observer) for observer in book.observers)
            self.unavailable_tree.insert(
                tk.END,
                f"{book.name} by {book.author} - Popularity: {book.popularity} - Observers: {observers}"
            )

        tk.Button(
            self.window, text="Request Book", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
            command=self.request_selected_book
        ).pack(pady=10)

    def lend_selected_book(self):
        selected_index = self.available_tree.curselection()
        lender_name = self.lender_name_entry.get().strip()
        lender_phone = self.lender_phone_entry.get().strip()

        # Validate inputs
        if not selected_index:
            messagebox.showerror("Error", "No book selected!")
            return
        if not lender_name or not lender_phone:
            messagebox.showerror("Error", "Lender details are required!")
            return
        try:
            lender_phone = int(lender_phone)  # Ensure phone number is numeric
        except ValueError:
            messagebox.showerror("Error", "Phone number must be numeric!")
            return

        # Get selected book
        selected_book = self.available_books[selected_index[0]]

        try:
            # Lend the book using LibraryManager
            self.library_manager.lend_book(selected_book.name, selected_book.author, lender_name, lender_phone)
            messagebox.showinfo("Success", f"Book '{selected_book.name}' lent successfully!")
            # Refresh available books
            self.available_books = self.library_manager.list_available_books()
            self.refresh_book_list(self.available_tree, self.available_books)
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def request_selected_book(self):
        selected_index = self.unavailable_tree.curselection()
        requester_name = self.requester_name_entry.get().strip()
        requester_phone = self.requester_phone_entry.get().strip()

        # Validate inputs
        if not selected_index:
            messagebox.showerror("Error", "No book selected!")
            return
        if not requester_name or not requester_phone:
            messagebox.showerror("Error", "Requester details are required!")
            return
        try:
            requester_phone = int(requester_phone)  # Ensure phone number is numeric
        except ValueError:
            messagebox.showerror("Error", "Phone number must be numeric!")
            return

        # Get selected book
        selected_book = self.unavailable_books[selected_index[0]]

        try:
            # Request the book using LibraryManager
            self.library_manager.request_book(selected_book.name, requester_name, requester_phone)
            messagebox.showinfo("Success", f"Request for book '{selected_book.name}' submitted successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

            self.refresh_book_list(self.unavailable_tree, self.unavailable_books)

    def refresh_book_list(self, tree, book_list):
        tree.delete(0, tk.END)  # Clear the listbox
        for book in book_list:
            tree.insert(tk.END, f"{book.name} by {book.author} - Copies: {book.copies if hasattr(book, 'copies') else book.popularity}")
