import unittest
import tempfile
import os
from Managment.UserManager import UserManager
import hashlib

#This tester tests UserManager.py functionality

class TestUserManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.users_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
        self.users_file.write("username,password_hash,Notifications\n")
        self.users_file.write(f"john_doe,{self.hash_password('hello')},[]\n")  # "hello" hashed
        self.users_file.close()

        # Initialize UserManager with the temporary file
        self.user_manager = UserManager(users_file=self.users_file.name)

    def tearDown(self):
        # Remove the temporary file after the test
        os.unlink(self.users_file.name)

    def test_hash_password(self):
        password = "hello"
        hashed = self.user_manager.hash_password(password)
        self.assertNotEqual(hashed, password)

    def test_get_user_by_username(self):
        user = self.user_manager.get_user_by_username("john_doe")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "john_doe")
        self.assertEqual(user.Notifications, [])

    def test_get_user_by_invalid_username(self):
        user = self.user_manager.get_user_by_username("invalid_user")
        self.assertIsNone(user)


    def test_validate_login_failure(self):
        result = self.user_manager.validate_login("john_doe", "wrong_password")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid username or password")

    def test_validate_login_nonexistent_user(self):
        result = self.user_manager.validate_login("nonexistent_user", "hello")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Invalid username or password")

    def test_validate_login_success(self):
        result = self.user_manager.validate_login("john_doe", "hello")
        self.assertTrue(result["success"])

    def test_register_user_success(self):
        self.user_manager.register_user("jane_doe", "password123")
        # Verify the user was added

    def test_register_existing_user(self):
        result = self.user_manager.register_user("john_doe", "password123")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Username already exists")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    unittest.main()
