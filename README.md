# 📚 Welcome to the Library Management System by Guy Levy and Gal Maymon! 🌟

## 🚀 Instructions to Run the Project

### 🛠️ Steps to Run

1. Navigate to the project folder.
2. Run `GUI.py` to launch the system:
   ```bash
   python GUI.py
   ```
3. Once launched, you will see the system's main menu, where you can:

   - ➕ Add, ➖ remove, or 🔄 lend books.
   - 📥 Request lent-out books.
   - 📝 Register and 🔐 log in librarians.
   - 🔍 View books by category or search for specific books.
   - 📤 Return books and view 🔔 notifications.
   - 🌟 View the most popular books.

   - Add, remove, or lend books.
   - Request lent-out books.
   - Register and log in librarians.
   - View books by category or search for specific books.
   - Return books and view notifications.
   - View the most popular books.

## 🛠️ System Attributes

### 🌟 Core Features

#### 👤 User Management:

- **Register Users**: Users can register with a username and password. Passwords are hashed for security.
- **Login**: Validate users with their username and hashed password.
- **Notifications**: Users receive notifications for due books, system updates, etc.

#### 📚 Book Management:

- **Add Books**: Add new books to the library with attributes like title, author, genre, year, and copies.
- **Remove Books**: Remove books from the library by title and author.
- **Lend Books**: Lend a book to a user, updating its loaned status and popularity.
- **Return Books**: Return a borrowed book, incrementing its availability.
- **View Books**: Display books in the library, search for specific books, or view books grouped by category.

### ⚙️ System Features

- **Logs**: Actions like adding, removing, or lending books are logged in `LibraryLog.txt`.
- **- **Data Persistence**: User and book data are stored in CSV files (`users.csv`, `books.csv`, `loaned_books.csv`).

### 🧪 Tests
- The project includes a `TESTS` folder containing automated test files to ensure the correctness of core functionalities.**: User and book data are stored in CSV files (`users.csv`, `books.csv`, `loaned_books.csv`).

## 🔧 Design Patterns and Concepts Used

### 1. **🧩 Decorator**

- **Usage**: The `@require_login` decorator ensures that critical actions like adding, removing, or lending books are accessible only to logged-in users.
- **Implementation**:
  ```python
  def require_login(func):
      def wrapper(self, *args, **kwargs):
          if not self.current_user:
              messagebox.showerror("Error", "You must be logged in to perform this action!")
              return
          return func(self, *args, **kwargs)
      return wrapper
  ```
- **Example**:
  ```python
  @require_login
  def add_book(self):
      AddBookWindow(self.root, self.library_manager)
  ```

### 2. **🔁 Iterator**

- **Usage**: Iterators are used to loop through books and users for searching, grouping by category, and filtering.
- **Implementation**:
  ```python
  def group_books_by_category(self):
      grouped_books = {}
      for book in self.books:  # Iterate over the list of Book objects
          if book.category not in grouped_books:
              grouped_books[book.category] = []
          grouped_books[book.category].append(book)
      return grouped_books
  ```
- **Example**: This is used to group books by their genre and display them in the `Category Display` window.

### 3. **📖 Dictionary**

- **Usage**: Dictionaries are used extensively for:
  - Grouping books by category.
  - Representing user notifications.
  - Loading and storing user and book data.
- **Implementation**:
  ```python
  grouped_books = {
      "Fantasy": [Book1, Book2],
      "Science Fiction": [Book3],
      "Romance": [Book4, Book5],
  }
  ```
- **Example**:
  ```python
  def get_user_by_username(self, username):
      with open(self.users_file, mode="r") as file:
          reader = csv.DictReader(file)
          for row in reader:
              if row["username"] == username:
                  return User(username=row["username"], password=row["password_hash"], Notifcations=json.loads(row.get("Notifcations", "[]")))
  ```

