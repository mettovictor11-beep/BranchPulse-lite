
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


  
def get_all_records():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM performance_records
            ORDER BY report_date DESC
        """)

        records = cursor.fetchall()
        connection.close()

        return records

    except sqlite3.Error as error:
        print("Could not retrieve records:", error)
        return []

  
def update_record(record_id, record):
    if not record.is_valid():
        print("Invalid performance record!")
        return

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE performance_records
            SET branch_name = ?,
                report_date = ?,
                performance_type = ?,
                target = ?,
                actual = ?,
                notes = ?
            WHERE id = ?
        """, (
            record.branch_name,
            record.report_date,
            record.performance_type,
            record.target,
            record.actual,
            record.notes,
            record_id
        ))

        connection.commit()

        if cursor.rowcount > 0:
            print("Performance record updated successfully!")
        else:
            print("No record found with that ID.")

        connection.close()

    except sqlite3.Error as error:
        print("Could not update record:", error)
    

def delete_record(record_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM performance_records
            WHERE id = ?
        """, (record_id,))

        connection.commit()

        if cursor.rowcount > 0:
            print("Performance record deleted successfully!")
        else:
            print("No record found with that ID.")

        connection.close()

    except sqlite3.Error as error:
        print("Could not delete record:", error)
