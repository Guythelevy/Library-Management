import csv
import hashlib
import logging
from Managment.User import User
import json

# This class is for managing users using the users.csv file
# Here you can find methods like hashing password, logging in and registering
# You can test this class using UserManagerTester.py in Tests folder

class UserManager:
    def __init__(self, users_file="CSV/users.csv"):
        self.users_file = users_file

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user_by_username(self, username):
        try:
            with open(self.users_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        # Create a User object from the row
                        return User(username=row["username"], password="",
                                    Notifications=json.loads(row.get("Notifications", "[]")))
        except FileNotFoundError:
            logging.error("User file not found.")
            return None
        return None

    def validate_login(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            with open(self.users_file, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    # Check if the row has at least two columns
                    if len(row) < 2:
                        continue  # Skip incomplete rows
                    if row[0] == username and row[1] == hashed_password:
                        logging.info("logged in successfully")
                        return {"success": True, "message": "Login successful"}
        except FileNotFoundError:
            logging.info("logged in fail")
            return {"success": False, "message": "User database not found"}
        logging.info("logged in fail")
        return {"success": False, "message": "Invalid username or password"}

    def register_user(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            # Check if the username already exists
            with open(self.users_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        logging.info("registered fail")
                        return {"success": False, "message": "Username already exists"}

            # Add the new user with an empty Notifications list
            with open(self.users_file, mode="a", newline="") as file:
                fieldnames = ["username", "password_hash", "Notifications"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                # If the file is empty, write the header first
                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow({
                    "username": username,
                    "password_hash": hashed_password,
                    "Notifications": json.dumps([])  # Default empty Notifications list
                })

            logging.info("registered successfully")
            return {"success": True, "message": "Registration successful"}

        except FileNotFoundError:
            # If file doesn't exist, create it and add the user
            with open(self.users_file, mode="w", newline="") as file:
                fieldnames = ["username", "password_hash", "Notifications"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({
                    "username": username,
                    "password_hash": hashed_password,
                    "Notifications": json.dumps([])  # Default empty Notifications list
                })

            logging.info("registered successfully")
            return {"success": True, "message": "User database created and user registered"}

        except Exception as e:
            logging.error(f"Error registering user: {e}")
            logging.info("registered fail")
            return {"success": False, "message": f"An error occurred: {e}"}
