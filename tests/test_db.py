import unittest
from database.db import get_connection

class TestDatabaseConnection(unittest.TestCase):

    def test_connection(self):
        conn = get_connection()

        # bağlantı oluştu mu?
        self.assertIsNotNone(conn)

        conn.close()

    def test_users_table(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users")

        rows = cursor.fetchall()

        # Sonuç liste mi?
        self.assertIsInstance(rows, list)

        conn.close()


if __name__ == "__main__":
    unittest.main()