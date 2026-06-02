import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=VICTUS;"
        "Database=VisionDeskDB;"
        "Trusted_Connection=yes;"
    )

# TEST
if __name__ == "__main__":
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users")

        for row in cursor:
            print(row)

        print("✅ Bağlantı başarılı")

    except Exception as e:
        print("❌ Hata:", e)