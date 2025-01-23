import tkinter as tk
from tkinter import ttk
import logging

class ViewBooksWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.books = self.library_manager.list_all_books()
        self.window = tk.Toplevel(parent)
        self.window.title("View Books")
        self.window.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10, fill=tk.X)

        tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: self.search_books(search_entry.get())).pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Category Display", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=self.display_books_by_category).pack(side=tk.LEFT, padx=5)


        self.tree = ttk.Treeview(self.window, columns=("Title", "Author", "Year", "Genre", "Copies"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Copies", text="Copies")

        self.tree.column("Title", width=120)
        self.tree.column("Author", width=120)
        self.tree.column("Year", width=80)
        self.tree.column("Genre", width=100)
        self.tree.column("Copies", width=80)

        self.populate_tree(self.books)

    def populate_tree(self, book_list):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            for book in book_list:
                self.tree.insert("", tk.END, values=(book.name, book.author, book.year, book.category, book.copies))
            logging.info("Displayed all books successfully")
        except Exception as e:
            logging.info("Displayed all books fail")

    def search_books(self, query):
        filtered_books = self.library_manager.search_books(query)
        self.populate_tree(filtered_books)

    def display_books_by_category(self):
        category_window = tk.Toplevel(self.window)
        category_window.title("Books by Category")
        category_window.geometry("600x500")

        # Search Frame
        search_frame = tk.Frame(category_window)
        search_frame.pack(pady=10, fill=tk.X)

        tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT,
                                                                                                          padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Treeview for displaying books
        tree = ttk.Treeview(category_window, columns=("Category", "Title", "Author", "Year", "Copies"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        tree.heading("Category", text="Category")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Year", text="Year")
        tree.heading("Copies", text="Copies")

        tree.column("Category", width=120)
        tree.column("Title", width=120)
        tree.column("Author", width=120)
        tree.column("Year", width=80)
        tree.column("Copies", width=80)

        def populate_tree(filtered_books):
            tree.delete(*tree.get_children())  # Clear the tree
            for category, books in filtered_books.items():
                for book in books:
                    tree.insert("", tk.END, values=(category, book.name, book.author, book.year, book.copies))

        # Get initial data
        grouped_books = self.library_manager.group_books_by_category()
        populate_tree(grouped_books)

        def search_books(query):
            query = query.lower()
            filtered_books = {}
            for category, books in grouped_books.items():
                matching_books = [
                    book for book in books if
                    query in book.name.lower() or
                    query in book.author.lower() or
                    query in category.lower()
                ]
                if matching_books:
                    filtered_books[category] = matching_books
            populate_tree(filtered_books)

        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: search_books(search_entry.get())).pack(side=tk.LEFT, padx=5)



