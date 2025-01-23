import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logging
from Managment import User


class ReturnBookWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.loaned_books = self.get_loaned_books()
        self.window = tk.Toplevel(parent)
        self.window.title("Return Book")
        self.window.geometry("800x600")
        self.create_widgets()

    def get_loaned_books(self):

        self.library_manager.load_loaned_books()
        return self.library_manager.loaned_books

    def create_widgets(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10, fill=tk.X)

        tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: self.search_books(search_entry.get())).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.window, columns=("Title", "Author", "Year", "Lender Name", "Lender Phone"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Lender Name", text="Lender Name")
        self.tree.heading("Lender Phone", text="Lender Phone")

        self.tree.column("Title", width=150)
        self.tree.column("Author", width=150)
        self.tree.column("Year", width=100)
        self.tree.column("Lender Name", width=150)
        self.tree.column("Lender Phone", width=150)

        self.populate_tree(self.loaned_books)

        tk.Label(self.window, text="", height=1).pack()  # Spacer

        tk.Button(self.window, text="Return Book", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                  command=self.return_selected_book).pack(pady=10)

    def populate_tree(self, loaned_books_list):
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Populate the tree with books
        for book in loaned_books_list:
            self.tree.insert("", tk.END, values=(book['title'], book['author'], book['year'], book['lender_name'], book['lender_phone']))

    def search_books(self, query):
        query = query.lower()
        filtered_books = [
            book for book in self.loaned_books
            if query in book['title'].lower() or query in book['author'].lower() or query in book['genre'].lower()
        ]
        self.populate_tree(filtered_books)

    def return_selected_book(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        selected_values = self.tree.item(selected_item[0], "values")
        title, author = selected_values[0], selected_values[1]

        try:
            # Return the book using the library manager
            self.library_manager.return_book(title, author)
            messagebox.showinfo("Success", f"Book '{title}' by {author} returned successfully!")

            # Refresh the list of loaned books
            self.loaned_books = self.get_loaned_books()
            self.populate_tree(self.loaned_books)
        except Exception as e:
            messagebox.showerror("Error", str(e))
