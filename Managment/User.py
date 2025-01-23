import hashlib
import csv
import json  # For saving and loading notifications

class User:
    def __init__(self, username, password, Notifications=None):
        self.username = username
        self.Notifications = Notifications if Notifications is not None else []
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.hash_password(password) == self.password_hash

    def add_Notification(self, message):
        self.Notifications.append(message)

    def get_Notifications(self):
        return self.Notification

    def get_Notifcations_num(self):
        return len(self.Notifications)

    @staticmethod
    def save_users_to_csv(users, filename="users.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password_hash", "Notifications"])
            for user in users:
                writer.writerow([
                    user.username,
                    user.password_hash,
                    json.dumps(user.Notifications)
                ])

    @staticmethod
    def load_users_from_csv(filename="users.csv"):
        users = []
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        user = User.__new__(User)
                        user.username = row["username"]
                        user.password_hash = row["password_hash"]
                        # Safely load Notifications
                        user.Notifications = json.loads(row["Notifications"]) if "Notifications" in row else []
                        users.append(user)
                    except (KeyError, json.JSONDecodeError) as e:
                        print(f"Error parsing row {row}: {e}")
        except FileNotFoundError:
            print(f"File '{filename}' not found. Returning an empty user list.")
        except Exception as e:
            print(f"Unexpected error while loading users: {e}")
        return users

