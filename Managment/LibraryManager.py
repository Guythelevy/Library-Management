import csv
import logging
import os


from Managment.Book import Book
from Managment.User import User

# This is the main class for managing the library. it uses books.csv file and loaned_books.csv
# You can find methods for adding books, removing books lending books and so
# You can test this class using LibraryManagerTester.py in Tests folder.

class LibraryManager:
    def __init__(self, books_file="CSV/books.csv", loaned_books_file="CSV/loaned_books.csv"):
        self.books_file = books_file
        self.loaned_books_file = loaned_books_file
        self.books = []
        self.loaned_books = []
        self.load_books()


    # Loads all books from the csv file
    def load_books(self):
        try:
            with open(self.books_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Check if 'popularity' and 'observers' columns exist
                if 'popularity' not in reader.fieldnames or 'observers' not in reader.fieldnames:
                    self.add_missing_columns(reader.fieldnames)
                    return  # Reload the file after adding missing columns


                self.books = [
                    Book(
                        author=row['author'],
                        name=row['title'],
                        year=int(row['year']),
                        category=row['genre'],
                        copies=int(row['copies']),
                        is_loaned=row['is_loaned'].lower() == 'true',
                        popularity=int(row['popularity']) if row.get('popularity') and row[
                            'popularity'].isdigit() else 0,
                        observers=Book.deserialize_observers(row.get('observers'))
                    ) for row in reader
                ]
            logging.info("Books loaded successfully.")
        except FileNotFoundError:
            self.books = []
            logging.warning("Books file not found. Starting with an empty library.")
        except Exception as e:
            logging.error(f"Error loading books: {e}")

    # Method for saving the books to the csv. used at every end of object-changing function
    def save_books(self):
        try:
            with open(self.books_file, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['author', 'title', 'year', 'genre', 'copies', 'is_loaned', 'popularity', 'observers']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                for book in self.books:
                    writer.writerow({
                        'author': book.author,
                        'title': book.name,
                        'year': book.year,
                        'genre': book.category,
                        'copies': book.copies,
                        'is_loaned': book.is_loaned,
                        'popularity': book.popularity,
                        'observers': book.serialize_observers()
                    })
        except Exception as e:
            logging.error(f"Failed to save books: {e}")

    #loads books from loaned_books.csv
    def load_loaned_books(self):
        try:
            self.loaned_books = []
            with open(self.loaned_books_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.loaned_books.append({
                        'author': row['author'],
                        'title': row['title'],
                        'year': int(row['year']),
                        'genre': row['genre'],
                        'lender_name': row['lender_name'],
                        'lender_phone': row['lender_phone']
                    })
            logging.info("Displayed borrowed books successfully.")
        except FileNotFoundError:
            self.loaned_books = []
            logging.warning("Loaned books file not found. Starting with an empty loaned books list.")
        except Exception as e:
            logging.info("Displayed borrowed books fail")

    def add_book(self, title, author, year, genre, copies):

        try:
            for book in self.books:
                if book.name == title and book.author == author:
                    book.add_copies(copies)
                    self.save_books()
                    logging.info(f"Added copies of existing book: {title} by {author}.")
                    return

            new_book = Book(author=author, name=title, year=year, category=genre, copies=copies, is_loaned=False, popularity=0, observers=[])
            self.books.append(new_book)
            self.save_books()
            logging.info("book added successfully")

        except Exception as e:
            logging.error("book added failed")

    def remove_book(self, title, author):
        try:
            for loaned_book in self.loaned_books:
                if loaned_book['title'] == title:
                    logging.warning(f"Cannot remove book '{title}' by {author} as it is currently loaned.")
                    raise ValueError(f"Cannot remove book '{title}' by {author} because it is currently loaned.")
            self.books = [book for book in self.books if not (book.name == title and book.author == author)]
            self.save_books()
            logging.info("book removed successfully")
        except Exception as e:
            logging.error("book removed failed")

    def lend_book(self, title, author, lender_name, lender_phone):
        try:
            for book in self.books:
                if book.name == title and book.author == author:
                    if book.loan():
                        self.save_books()
                        self.log_loaned_book(book, lender_name, lender_phone)
                        logging.info("book borrowed successfully")
                    return
            logging.warning(f"Book not found or unavailable: {title} by {author}.")
        except Exception as e:
            logging.info("book borrowed fail")

    def return_book(self, title, author):
        try:
            self.load_loaned_books()
            for loaned_book in self.loaned_books:
                if loaned_book['title'] == title and loaned_book['author'] == author:
                    for book in self.books:
                        if book.name == title and book.author == author:
                            book.return_loan()
                            self.save_books()

                    # Update loaned_books to exclude the returned book
                    self.loaned_books = [
                        book for book in self.loaned_books
                        if not (book['title'] == title and book['author'] == author)
                    ]

                    # Save updated loaned_books to CSV
                    self.save_loaned_books()
                    logging.info("book returned successfully")

                    # Notify all users that the book is available
                    try:
                        users = User.load_users_from_csv("CSV/users.csv")  # Use the correct path
                        for user in users:
                            user.add_Notification(f"Book '{title}' by {author} is now available to lend!")
                            logging.info(f"Notification added for user: {user.username}")

                        # Save updated users back to the CSV
                        User.save_users_to_csv(users, "CSV/users.csv")  # Save to the correct path
                        logging.info(f"Users notified about the return of book '{title}' by {author}.")
                    except Exception as e:
                        logging.error(f"Error notifying users about returned book: {e}")
                        raise RuntimeError("Failed to notify users about the returned book.")

                    return

            logging.warning(f"Book not found in loaned books: {title} by {author}.")
            raise ValueError(f"Book '{title}' by {author}' not found in loaned books.")
            logging.warning(f"Book not found in loaned books: {title} by {author}.")
            raise ValueError(f"Book '{title}' by {author}' not found in loaned books.")

        except Exception as e:
            logging.info("book returned fail")

    def request_book(self, title, requester_name, requester_phone):
        for book in self.books:
            if book.name.lower() == title.lower():
                # Add the requester to the watch list
                book.add_observer(requester_name)

                # Add Popularity
                book.IncermentPopularity()

                self.save_books()


    def list_available_books(self):
        return [book for book in self.books if book.copies > 0]

    def list_all_books(self):
        return [book for book in self.books]

    def list_popular_books(self, threshold=10):
        try:
            logging.info("displayed successfully")
            return [book for book in self.books if book.popularity >= threshold]
        except Exception as e:
            logging.info("displayed fail")

    def list_unavailable_books(self):
        return [book for book in self.books if book.copies == 0]

    def search_books(self, query):
        query = query.lower()
        logging.info(f"Search book '{query}' by name completed successfully")
        return [
            book for book in self.books
            if query in book.name.lower() or query in book.author.lower() or query in book.category.lower()
        ]

    def log_loaned_book(self, book, lender_name, lender_phone):

        loaned_books_file = "CSV/loaned_books.csv"
        fieldnames = ['title', 'author', 'year', 'genre', 'lender_name', 'lender_phone']

        try:
            # Check if the file exists to write the header only if it doesn't
            write_header = not os.path.exists(loaned_books_file)

            with open(loaned_books_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if write_header:
                    writer.writeheader()

                writer.writerow({
                    'title': book.name,
                    'author': book.author,
                    'year': book.year,
                    'genre': book.category,
                    'lender_name': lender_name,
                    'lender_phone': lender_phone,
                })

            logging.info(f"Logged loaned book: {book.name} by {book.author} to {lender_name}.")
        except Exception as e:
            logging.error(f"Failed to log loaned book: {e}")

    def group_books_by_category(self):
        try:
            grouped_books = {}
            for book in self.books:
                if book.category not in grouped_books:
                    grouped_books[book.category] = []
                grouped_books[book.category].append(book)
            logging.info("Displayed book by category successfully.")
            return grouped_books
        except Exception as e:logging.info("Displayed book by category fail.")


    def save_loaned_books(self):
        try:
            with open(self.loaned_books_file, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['title', 'author', 'year', 'genre', 'lender_name', 'lender_phone']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.loaned_books)
            logging.info("Loaned books saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save loaned books: {e}")

    def add_missing_columns(self, existing_fieldnames):
        new_fieldnames = existing_fieldnames[:]
        if 'popularity' not in existing_fieldnames:
            new_fieldnames.append('popularity')
        if 'observers' not in existing_fieldnames:
            new_fieldnames.append('observers')

        try:
            with open(self.books_file, mode='r', newline='', encoding='utf-8') as infile:
                reader = csv.DictReader(infile)
                rows = [row for row in reader]

            with open(self.books_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
                writer.writeheader()

                for row in rows:
                    # Add default values for missing columns
                    row.setdefault('popularity', '0')
                    row.setdefault('observers', '[]')
                    writer.writerow(row)

            logging.info("Added missing columns to books.csv.")
        except Exception as e:
            logging.error(f"Error adding missing columns: {e}")

