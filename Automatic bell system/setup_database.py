import mysql.connector
from mysql.connector import Error


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Password@123"
DB_NAME = "school_bell_db"


def create_database():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        print(f"Database '{DB_NAME}' is ready.")

        cursor.close()
        connection.close()

    except Error as e:
        print("Error while creating database:", e)


def create_tables():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        create_bell_schedule_table = """
            CREATE TABLE IF NOT EXISTS bell_schedule (
                schedule_id INT AUTO_INCREMENT PRIMARY KEY,
                period_name VARCHAR(50) NOT NULL,
                bell_time TIME NOT NULL,
                duration_seconds INT NOT NULL DEFAULT 10,
                days VARCHAR(50) NOT NULL,
                is_active TINYINT(1) NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

        create_bell_log_table = """
            CREATE TABLE IF NOT EXISTS bell_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                schedule_id INT NULL,
                period_name VARCHAR(50) NOT NULL,
                run_time DATETIME NOT NULL,
                bell_type ENUM('AUTO', 'MANUAL') NOT NULL,
                status VARCHAR(30) NOT NULL,

                FOREIGN KEY (schedule_id)
                    REFERENCES bell_schedule(schedule_id)
                    ON DELETE SET NULL
            )
        """

        cursor.execute(create_bell_schedule_table)
        print("Table 'bell_schedule' is ready.")

        cursor.execute(create_bell_log_table)
        print("Table 'bell_log' is ready.")

        connection.commit()

        cursor.close()
        connection.close()

    except Error as e:
        print("Error while creating tables:", e)


def insert_sample_schedules():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        check_query = "SELECT COUNT(*) FROM bell_schedule"
        cursor.execute(check_query)
        schedule_count = cursor.fetchone()[0]

        if schedule_count > 0:
            print("Sample schedules already exist. Skipping insertion.")
            cursor.close()
            connection.close()
            return

        sample_schedules = [
            ("Morning Assembly", "08:45:00", 15, "MON,TUE,WED,THU,FRI", 1),
            ("Period 1", "09:00:00", 10, "MON,TUE,WED,THU,FRI", 1),
            ("Period 2", "09:50:00", 10, "MON,TUE,WED,THU,FRI", 1),
            ("Short Break", "10:40:00", 10, "MON,TUE,WED,THU,FRI", 1),
            ("Period 3", "10:55:00", 10, "MON,TUE,WED,THU,FRI", 1),
            ("Lunch Break", "12:30:00", 20, "MON,TUE,WED,THU,FRI", 1),
            ("Dispersal", "15:30:00", 25, "MON,TUE,WED,THU,FRI", 1)
        ]

        insert_query = """
            INSERT INTO bell_schedule
            (period_name, bell_time, duration_seconds, days, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.executemany(insert_query, sample_schedules)
        connection.commit()

        print(f"{cursor.rowcount} sample schedules inserted successfully.")

        cursor.close()
        connection.close()

    except Error as e:
        print("Error while inserting sample schedules:", e)


def show_tables():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")

        tables = cursor.fetchall()

        print("\nTables in database:")
        for table in tables:
            print("-", table[0])

        cursor.close()
        connection.close()

    except Error as e:
        print("Error while showing tables:", e)


if __name__ == "__main__":
    print("=" * 50)
    print("SETTING UP AUTOMATIC SCHOOL BELL DATABASE")
    print("=" * 50)

    create_database()
    create_tables()
    insert_sample_schedules()
    show_tables()

    print("\nDatabase setup completed successfully.")
