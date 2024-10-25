import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import sqlite3
import streamlit as st
from database_utils import connect_db

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
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM clients')
        rows = cursor.fetchall()
       
        
        if not rows:
            st.write("No clients found.")
            return
        #Convert the fetched data into dataframe
        df = pd.DataFrame(rows, columns=['ID', 'Name', 'Age', 'Weight', 'Goals'])     
        df['Age'] = df['Age'].astype(int)
        df['Weight'] = df['Weight'].astype(float).map('{:.2f} lbs'.format)
        
        
        search_name = st.text_input("Search by Name")
        if search_name:
            df = df[df['Name'].str.contains(search_name, case=False, na=False)]
        #build grid option
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_default_column(editable=False, groupable=True)
        grid_options = gb.build()
        
        st.write("Client List:")
        AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='clients.csv',
            mime='text/csv',
)

    
    except sqlite3.Error as e:
        st.error(f"Error fetching client data: {e}")
        print(f"Error fetching client data: {e}")
    finally:
        conn.close()
        

def delete_client(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()
    st.write(f"Client with ID {client_id} has been deleted")
