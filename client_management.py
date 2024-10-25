import sqlite3
import streamlit as st

def connect_db():
    return sqlite3.connect('trainer_app.db')

def add_client(name, age, weight, goals):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        
        cursor.execute('''
                   INSERT INTO clients (name, age, weight, goals)
                   VALUES (?, ?, ?, ?)
                   ''', (name, age, weight, goals))
        conn.commit()
       
        st.success(f"Client '{name}' added successfully!")
        print("Client added:", name, age, weight, goals)
    except sqlite3.Error as e:
        st.error(f"Error inserting client data: {e}")
        print(f"Error inserting client data: {e}")
    finally:
        conn.close()
    
@st.cache_data(show_spinner=False, ttl=0)
def fetch_all_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    rows = cursor.fetchall()
    conn.close()
    return rows
    
def view_clients():
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Fetch all clients
        cursor.execute('SELECT * FROM clients')
        rows = cursor.fetchall()

        # Debugging: Check if rows are fetched
        print("Fetched clients in view_clients function:", rows)  # Terminal output
        st.text(f"Debug - Number of clients fetched: {len(rows)}")  # Streamlit output

        # Check if there are any clients to show
        if not rows:
            st.write("No clients found.")
            return

        # Display each client's data
        st.write("Client List:")
        for row in rows:
            st.write(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Weight: {row[3]} lbs, Goals: {row[4]}")
    except sqlite3.Error as e:
        st.error(f"Error fetching client data: {e}")
        print(f"Error fetching client data: {e}")  # Terminal output
    finally:
        # Ensure the connection is closed
        conn.close()


def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor() 
    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()
    st.write(f"Client with ID {client_id} has been deleted")
        