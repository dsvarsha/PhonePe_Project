import mysql.connector
from mysql.connector import Error

# ---------- CONNECTION SETTINGS ----------
HOST = "localhost"
USER = "root"
PASSWORD = "varsha2003"     # <-- your MySQL password
DATABASE = "phonepe_db"
# -----------------------------------------

# ✅ Define connection safely before the try block
connection = None

try:
    print("🔄 Trying to connect to MySQL...")
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

    if connection.is_connected():
        print("✅ Connection successful!")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"📂 Connected to database:", db_name[0])
        cursor.close()

except Error as e:
    print("❌ Error connecting to MySQL:", e)

finally:
    # ✅ Check properly before using .is_connected()
    if connection is not None and connection.is_connected():
        connection.close()
        print("🔒 MySQL connection closed.")
    else:
        print("⚠️ Connection was never established, nothing to close.")
