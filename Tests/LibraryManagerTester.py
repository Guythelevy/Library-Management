import unittest
import tempfile
import os
from Managment.LibraryManager import LibraryManager

#This tester tests LibraryManager.py functionality

class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        # Create temporary CSV files for testing
        self.books_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.loaned_books_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.users_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')

        # Write headers for books.csv
        self.books_file.write("author,title,year,genre,copies,is_loaned,popularity,observers\n")
        self.books_file.write("J.K. Rowling,Harry Potter,1997,Fantasy,5,false,0,[]\n")
        self.books_file.close()

        # Write headers for loaned_books.csv
        self.loaned_books_file.write("title,author,year,genre,lender_name,lender_phone\n")
        self.loaned_books_file.write("Harry Potter,J.K. Rowling,1997,Fantasy,John Doe,1234567890\n")
        self.loaned_books_file.close()

        # Write headers for users.csv
        self.users_file.write("username,password_hash,Notifications\n")
        self.users_file.write("john_doe,some_hash,[]\n")
        self.users_file.write("jane_smith,another_hash,[]\n")
        self.users_file.close()

        # Initialize LibraryManager with test files
        self.manager = LibraryManager(
            books_file=self.books_file.name,
            loaned_books_file=self.loaned_books_file.name
        )

    def tearDown(self):
        # Remove temporary files after tests
        os.unlink(self.books_file.name)
        os.unlink(self.loaned_books_file.name)
        os.unlink(self.users_file.name)

    def test_load_books(self):
        self.manager.load_books()
        self.assertEqual(len(self.manager.books), 1)
        self.assertEqual(self.manager.books[0].name, "Harry Potter")

    def test_lend_book(self):
        self.manager.lend_book("Harry Potter", "J.K. Rowling", "Alice", "123456789")
        self.manager.load_loaned_books()
        self.assertEqual(self.manager.books[0].copies, 4) #Copies reduced by 1

    def test_return_book(self):
        self.manager.return_book("Harry Potter", "J.K. Rowling")
        self.manager.load_loaned_books()
        self.assertEqual(len(self.manager.loaned_books), 0)  # Loan should be removed

    def test_add_book(self):
        self.manager.add_book("The Hobbit", "J.R.R. Tolkien", 1937, "Adventure", 3)
        self.assertEqual(self.manager.books[1].copies,3)  # Original + New Book

    def test_remove_book(self):
        self.manager.remove_book("Harry Potter", "J.K. Rowling")
        self.assertEqual(len(self.manager.books), 0)  # Book should be removed

    def test_request_book(self):
        self.manager.request_book("Harry Potter", "Alice", "123456789")
        self.assertIn("Alice", self.manager.books[0].observers)

if __name__ == "__main__":
    unittest.main()
