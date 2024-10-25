import sqlite3
import os

def connect_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer_app.db')
    print(f"Database path used for connection: {db_path}")  # Debug: Confirm the database path
    return sqlite3.connect(db_path)

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Create or verify 'clients' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                weight REAL NOT NULL,
                goals TEXT
            )
        ''')

        # Create or verify 'workouts' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                exercise TEXT NOT NULL,
                weight REAL NOT NULL,
                reps INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(client_id) REFERENCES clients(id)
            )
        ''')

        # Commit the changes
        conn.commit()
        print("Database initialized successfully, tables created or verified.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        # Ensure the connection is closed
        conn.close()

# Run the function if this script is executed
if __name__ == "__main__":
    initialize_db()
