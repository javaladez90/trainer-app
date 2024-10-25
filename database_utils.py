import sqlite3
import os
def connect_db():
    #Always use the absolute path relative to the files location
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainer_app.db')
    print(f"Database path used for connection: {db_path}")
    return sqlite3.connect(db_path)