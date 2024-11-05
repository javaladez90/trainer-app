# authentication.py
import bcrypt
import sqlite3
import base64
from database_utils import connect_db

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def add_user(username, name, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    # Corrected line: Use 'hashed_password' variable, not 'hash_password' function
    hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
    try:
        cursor.execute('''
            INSERT INTO users (username, name, password, role)
            VALUES (?, ?, ?, ?)
        ''', (username, name, hashed_password_str, role))
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."
    except sqlite3.Error as e:
        return False, f"Error adding user: {e}"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT password, role FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result:
            hashed_password_str, role = result
            # Decode the base64 string back to bytes
            hashed_password = base64.b64decode(hashed_password_str.encode('utf-8'))
            if verify_password(password, hashed_password):
                return role  # Return user role
    except sqlite3.Error as e:
        print(f"Error during authentication: {e}")
    finally:
        conn.close()
    return None
