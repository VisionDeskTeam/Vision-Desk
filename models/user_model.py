from database.db import get_connection

def get_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Users WHERE username=? AND password=?",
        (username, password)
    )

    return cursor.fetchone()