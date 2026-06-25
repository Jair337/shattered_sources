import sqlite3
# Import db_path directly from your config to ensure you are checking the right file
from config import db_path_seerist


def verify_database():
    print(f"Checking database at: {db_path_seerist}")

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path_seerist)
        cursor = conn.cursor()

        # 1. Query to count total records
        cursor.execute("SELECT COUNT(*) FROM events_seerist_raw;")
        total_rows = cursor.fetchone()[0]
        print(f"📊 Total records in 'events_seerist_raw': {total_rows}")

        # 2. Query to fetch the first sample row to check columns
        if total_rows > 0:
            cursor.execute("SELECT event_id, title, category FROM events_seerist_raw LIMIT 1;")
            sample = cursor.fetchone()
            print("\n✅ Sample Data Found:")
            print(f"   ID: {sample[0]}")
            print(f"   Title: {sample[1]}")
            print(f"   Category: {sample[2]}")
        else:
            print("\n❌ The table exists, but it is completely empty.")

        conn.close()

    except sqlite3.OperationalError as e:
        print(f"\n❌ Database error: {e}")
        print("This usually means the table 'events_seerist_raw' does not exist yet.")


if __name__ == "__main__":
    verify_database()