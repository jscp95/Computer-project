from datetime import datetime

import mysql.connector
from mysql.connector import Error

from backend.database import get_connection


def save_bell_log(schedule_id, period_name, bell_type, status="SUCCESS"):
    conn = get_connection()

    if not conn:
        return False, "Database connection failed"

    cursor = None

    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO bell_log
            (schedule_id, period_name, run_time, bell_type, status)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            schedule_id,
            period_name,
            datetime.now(),
            bell_type,
            status
        )

        cursor.execute(query, values)
        conn.commit()

        return True, "Bell log saved"

    except Error as e:
        print("MySQL error while saving bell log:")
        print(e)

        return False, f"Error saving bell log: {e}"

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()
