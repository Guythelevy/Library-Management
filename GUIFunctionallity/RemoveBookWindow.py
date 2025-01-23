import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class RemoveBookWindow:
    def __init__(self, parent, library_manager):
        self.library_manager = library_manager
        self.books = self.library_manager.list_all_books()
        self.window = tk.Toplevel(parent)
        self.window.title("Remove Book")
        self.window.geometry("800x700")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Select a Book to Remove:", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white"
                 ).pack(pady=5)

        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10, fill=tk.X)

        tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  command=lambda: self.search_books(search_entry.get())).pack(side=tk.LEFT, padx=5)

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

        tk.Label(self.window, text="", height=1).pack()  # Spacer

        tk.Button(
            self.window, text="Remove Book", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
            command=self.remove_selected_book
        ).pack(pady=10)

    def populate_tree(self, book_list):
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Populate the tree with books
        for book in book_list:
            self.tree.insert("", tk.END, values=(book.name, book.author, book.year, book.category, book.copies))

    def search_books(self, query):
        query = query.lower()
        filtered_books = [
            book for book in self.books
            if query in book.name.lower() or query in book.author.lower() or query in book.category.lower()
        ]
        self.populate_tree(filtered_books)

    def remove_selected_book(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        selected_values = self.tree.item(selected_item[0], "values")
        title, author = selected_values[0], selected_values[1]

        try:
            # Call the LibraryManager's remove_book method
            self.library_manager.remove_book(title, author)
            messagebox.showinfo("Success", f"Book '{title}' by {author} removed successfully!")
        except ValueError as e:  # Handle loaned book error
            messagebox.showerror("Error", str(e))
        except Exception as e:  # Handle other errors
            messagebox.showerror("Error", f"Failed to remove book: {e}")
        finally:
            # Refresh the list of books
            self.books = self.library_manager.list_all_books()
            self.populate_tree(self.books)
