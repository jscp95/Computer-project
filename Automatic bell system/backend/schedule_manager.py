from backend.database import get_connection


def add_schedule(period_name, bell_time, duration_seconds, days, is_active=True):
    conn = get_connection()

    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO bell_schedule
            (period_name, bell_time, duration_seconds, days, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            period_name,
            bell_time,
            duration_seconds,
            days,
            1 if is_active else 0
        )

        cursor.execute(query, values)
        conn.commit()

        return True, "Schedule added successfully"

    except Error as e:
        return False, f"Error adding schedule: {e}"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_all_schedules():
    conn = get_connection()

    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT schedule_id, period_name, bell_time,
                   duration_seconds, days, is_active
            FROM bell_schedule
            ORDER BY bell_time
        """

        cursor.execute(query)
        schedules = cursor.fetchall()

        for schedule in schedules:
            schedule["bell_time"] = str(schedule["bell_time"])
            schedule["is_active"] = bool(schedule["is_active"])

        return schedules

    except Error as e:
        print("Error fetching schedules:", e)
        return []

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def update_schedule(schedule_id, period_name, bell_time, duration_seconds, days, is_active):
    conn = get_connection()

    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()

        query = """
            UPDATE bell_schedule
            SET period_name = %s,
                bell_time = %s,
                duration_seconds = %s,
                days = %s,
                is_active = %s
            WHERE schedule_id = %s
        """

        values = (
            period_name,
            bell_time,
            duration_seconds,
            days,
            1 if is_active else 0,
            schedule_id
        )

        cursor.execute(query, values)
        conn.commit()

        return True, "Schedule updated successfully"

    except Error as e:
        return False, f"Error updating schedule: {e}"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def delete_schedule(schedule_id):
    conn = get_connection()

    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()

        query = "DELETE FROM bell_schedule WHERE schedule_id = %s"
        cursor.execute(query, (schedule_id,))
        conn.commit()

        return True, "Schedule deleted successfully"

    except Error as e:
        return False, f"Error deleting schedule: {e}"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def toggle_schedule(schedule_id, new_status):
    conn = get_connection()

    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()

        query = """
            UPDATE bell_schedule
            SET is_active = %s
            WHERE schedule_id = %s
        """

        cursor.execute(query, (1 if new_status else 0, schedule_id))
        conn.commit()

        return True, "Schedule status updated"

    except Error as e:
        return False, f"Error updating status: {e}"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
