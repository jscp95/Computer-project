import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Password@123",
    "database": "school_bell_db"
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("Database connection error:", e)
        return None


def test_connection():
    conn = get_connection()

    if conn and conn.is_connected():
        conn.close()
        return True, "MySQL connected successfully"

    return False, "Could not connect to MySQL"
