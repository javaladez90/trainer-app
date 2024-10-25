import streamlit as st 
from client_management import add_client, view_clients, delete_client
from initialization import initialize_db

#initialize the database at start up

initialize_db()

st.title('Fuerza Fitness')

# Sidebar menu for navigation 
menu = ["Add Client", "View Client", "Delete Client"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Client":
    st.subheader("Add a New Client")
    st.write("Selected: Add Client")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    weight = st.number_input("Weight (lbs)", min_value=0)
    goals = st.text_area("Goals")
    
    if st.button("Add Client"):
        if name:
            add_client(name, age, weight, goals)
            st.success(f"Client '{name}' add successfully!")
        else:
            st.error("Please enter a name.")
            
elif choice == "View Clients":
    st.subheader("All Clients")
    st.write("Attempting to view clients...")
    view_clients()
    
elif choice == "Delete Client":
    st.subheader("Delete a Client")
    client_id = st.text_input("Client ID to delete")
    
    if st.button("Delete Client"):
        if client_id.isdigit():
            delete_client(int(client_id))
        else: 
            st.error("Please enter a valid client ID")