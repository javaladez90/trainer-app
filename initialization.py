import sqlite3
import os
from database_utils import connect_db



    
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

        #Create table for workout_plans
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS workout_plans (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           description TEXT
                       )
                       ''')
        
        # Create or verify 'workouts' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_plan_id INTEGER,
                name TEXT NOT NULL,
                sets REAL NOT NULL,
                reps INTEGER NOT NULL,
                weight TEXT NOT NULL,
                FOREIGN KEY(workout_plan_id) REFERENCES workout_plans(id)
            )
        ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT UNIQUE NOT NULL,
                           name TEXT NOT NULL,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL
                       )
                       ''')

        #create assigned workout tables
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS workout_plans (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           description TEXT
                       )
                       ''')
        
        #create assigned_workouts table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS assigned_workouts (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           client_id integer,
                           workout_plan_id INTEGER,
                           assigned_date TEXT,
                           FOREIGN KEY(client_id) REFERENCES clients(id),
                           FOREIGN KEY(workout_plan_id) REFERENCES workout_plans(id)
                       )
                       ''')
        
        #create workout_logs
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS workout_logs (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           client_id INTEGER,
                           exercise_id INTEGER,
                           date TEXT,
                           sets_completed INTEGER
                           reps_completed INTEGER,
                           weight_used REAL,
                           FOREIGN KEY(client_id) REFERENCES clients(id),
                           FOREIGN KEY(exercise_id) REFERENCES exercises(id)
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
