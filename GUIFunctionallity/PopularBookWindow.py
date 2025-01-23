import tkinter as tk
from tkinter import ttk

class PopularBookWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.books = self.library_manager.list_popular_books()
        self.window = tk.Toplevel(parent)
        self.window.title("Popular Books")
        self.window.geometry("600x500")
        self.create_widgets()

    def create_widgets(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10, fill=tk.X)

        tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=self.search_books).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.window, columns=("Title", "Author", "Year", "Genre", "Popularity"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Popularity", text="Popularity")

        self.tree.column("Title", width=150)
        self.tree.column("Author", width=150)
        self.tree.column("Year", width=80)
        self.tree.column("Genre", width=100)
        self.tree.column("Popularity", width=100)

        self.populate_tree(self.books)

    def populate_tree(self, book_list):
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Populate the tree with books
        for book in book_list:
            self.tree.insert("", tk.END, values=(book.name, book.author, book.year, book.category, book.popularity))

    def search_books(self):
        query = self.search_entry.get().strip().lower()
        filtered_books = [
            book for book in self.books
            if query in book.name.lower() or query in book.author.lower() or query in book.category.lower()
        ]
        self.populate_tree(filtered_books)
