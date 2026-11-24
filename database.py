
import sqlite3


DATABASE_NAME = "branchpulse.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                branch_name TEXT NOT NULL,
                report_date TEXT NOT NULL,
                performance_type TEXT NOT NULL,
                target REAL NOT NULL,
                actual REAL NOT NULL,
                notes TEXT
            )
        """)

        connection.commit()
        connection.close()

        print("Database table created successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


if __name__ == "__main__":
    create_table()



def add_record(record):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO performance_records (
                branch_name,
                report_date,
                performance_type,
                target,
                actual,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            record.branch_name,
            record.report_date,
            record.performance_type,
            record.target,
            record.actual,
            record.notes
        ))

        connection.commit()
        connection.close()

        print("Performance record added successfully!")

    except sqlite3.Error as error:
        print("Could not add record:", error)
