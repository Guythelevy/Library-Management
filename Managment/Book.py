import json

class Book:

    def __init__(self, author, name, year, category, copies, is_loaned, popularity, observers=None):
        self.author = author
        self.name = name
        self.year = year
        self.category = category
        self.copies = copies
        self.popularity = popularity
        self.is_loaned = is_loaned
        self.observers = observers or []  # Default to an empty list

    def add_copies(self, count):
        if count > 0:
            self.copies += count
            self.is_loaned = self.copies == 0
        else:
            raise ValueError("Count must be a positive integer.")

    def remove_copies(self, count):
        if count > 0 and count <= self.copies:
            self.copies -= count
            self.is_loaned = self.copies == 0
        elif count > self.copies:
            raise ValueError("Cannot remove more copies than are available.")
        else:
            raise ValueError("Count must be a positive integer.")

    def loan(self):
        if self.copies == 0:
            self.is_loaned = True
            print("Unavailable copies of this book.")
            return False
        else:
            self.copies -= 1
            self.popularity += 1
            self.is_loaned = self.copies == 0
            print(f"A copy of '{self.name}' has been loaned. Remaining copies: {self.copies}")
            return True

    def return_loan(self):
        self.copies += 1
        self.is_loaned = self.copies == 0

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, action):
        for observer in self.observers:
            print(f"Notifying {observer}: {action}")

    def serialize_observers(self):
        return json.dumps(self.observers)

    @staticmethod
    def deserialize_observers(observers_str):
        return json.loads(observers_str) if observers_str else []

    def IncermentPopularity(self):
        self.popularity += 1
