import tkinter as tk
from tkinter import messagebox

class AddBookWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.window = tk.Toplevel(parent)
        self.window.title("Add Book")
        self.window.geometry("300x400")
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.window, text="Title:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.title_entry = tk.Entry(self.window)
        self.title_entry.pack(pady=5)

        # Author
        tk.Label(self.window, text="Author:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.author_entry = tk.Entry(self.window)
        self.author_entry.pack(pady=5)

        # Year
        tk.Label(self.window, text="Year:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.year_entry = tk.Entry(self.window)
        self.year_entry.pack(pady=5)

        # Genre
        tk.Label(self.window, text="Genre:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.genre_entry = tk.Entry(self.window)
        self.genre_entry.pack(pady=5)

        # Copies
        tk.Label(self.window, text="Copies:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=5)
        self.copies_entry = tk.Entry(self.window)
        self.copies_entry.pack(pady=5)

        # Submit Button
        tk.Button(
            self.window,
            text="Submit",
            command=self.submit_book,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
        ).pack(pady=10)

    def submit_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        genre = self.genre_entry.get()
        copies = self.copies_entry.get()

        # Validate input
        if not all([title, author, year, genre, copies]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            year = int(year)
            copies = int(copies)
        except ValueError:
            messagebox.showerror("Error", "Year and Copies must be numbers!")
            return

        # Add the book using LibraryManager
        try:
            self.library_manager.add_book(title, author, year, genre, copies)
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
