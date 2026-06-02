from database.db import get_connection

def get_logs_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT posture_count, focus_time FROM Logs WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchall()