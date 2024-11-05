from authentication import authenticate_user, add_user
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from database_utils import connect_db
import streamlit as st 
from client_management import add_client, view_clients, delete_client, get_client_id_by_username
from initialization import initialize_db
from workout_management import (
    add_workout_plan, add_exercise, assign_workout_to_client,
    get_assigned_workouts, get_exercises_for_workout_plan,
    log_workout, get_workout_logs
)

#initialize the database at start up

initialize_db()


st.title('Fuerza Fitness')


#session state initialization
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
    st.session_state['username'] = ''
    st.session_state['role'] = ''
    
#Login
if not st.session_state['authentication_status']:
    st.sidebar.header('Login')
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input('Password', type='password')
    login_button = st.sidebar.button('Login')
    
    if login_button:
        role = authenticate_user(username, password)
        if role:
            st.session_state['authentication_status'] = True
            st.session_state['username'] = username
            st.session_state['role'] = role
            st.success(f"Logged in as {username} ({role})")
            st.rerun()
        else:
            st.error('Username/password is incorrect')
else:
    st.sidebar.write(f"Logged in as {st.session_state['username']} ({st.session_state['role']})")
    if st.sidebar.button('Logout'):
        st.session_state['authentication_status'] = False
        st.session_state['username'] = ''
        st.session_state['role'] = ''
        st.success("You have been logged out.")
        st.rerun()
        
if st.session_state['authentication_status']:
    if st.session_state['role'] == 'trainer':
        #sidebar menu
        menu = ["Add Client", "View Clients", "Delete Client", "Workout Plans", "Assign Workouts"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Workout Plans":
            st.subheader("Create a Workout Plan")
            plan_name = st.text_input("Workout Plan Name")
            plan_description = st.text_area("Description")
            if st.button("Create Workout Plan"):
                if plan_name:
                    workout_plan_id = add_workout_plan(plan_name, plan_description)
                    st.success(f"Workout plan '{plan_name}' created successfully!")
                    #add exercises to workout plan
                    st.subheader("Add exercises to the Workout Plan")
                    exercise_name = st.text_input("Exercise Name")
                    sets = st.number_input("Sets", min_value=1)
                    reps = st.number_input("Reps", min_value=1)
                    weight = st.number_input("Weight (lbs)", min_value=0)
                    if st.button("Add Exercise"):
                        if exercise_name:
                            add_exercise(workout_plan_id, exercise_name, sets, reps, weight)
                            st.success(f"Exercise '{exercise_name}' added to the workout plan.")
                        else:
                            st.error("Please enter an exercise name.")
            else:
                st.error("Please enter a workout plan name.")
        elif choice == "Asign Workouts":
            st.subheader("Addign Workout Plan to a Client")
            #assuming you have a function to get all clients
            clients = view_clients(return_data=True) #midify view_clients to retur ndata
            client_options = {client[1]: client[0] for client in clients} #{Name: ID}
            selected_client = st.selectbox("Select Client", list(client_options.keys()))
            client_id = client_options[selected_client]
            
            #assuming theres a get all workout plans
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM workout_plans')
            workout_plans = cursor.fetchall()
            conn.close()
            workout_plan_options = {plan[1]: plan[0] for plan in workout_plans}
            selected_plan = st.selectbox("Select Workout Plan", list(workout_plan_options.keys()))
            workout_plan_id = workout_plan_options[selected_plan]        
            
            if st.button("Assign Workout Plan"):
                assign_workout_to_client(client_id, workout_plan_id)
                st.success(f"Assigned workout plan '{selected_plan}' to client '{selected_client}'.")
                
            
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
                    st.success(f"Client '{name}' added successfuly!")
                else:
                    st.error("Please enter a name.")
            
        
        elif choice == "View Clients":
            st.subheader("All Clients")
            view_clients()
    
        elif choice == "Delete Client":
            st.subheader("Delete a Client")
            client_id = st.text_input("Client ID to delete")
    
            if st.button("Delete Client"):
                if client_id.isdigit():
                    delete_client(int(client_id))
                    st.success(f"Client with ID {client_id} has been deleted.")
                else: 
                    st.error("Please enter a valid client ID")
    else:
        st.subheader("Welcome to Your Dashboard")
        st.write("Client functionalities will be implemented here.")

elif st.session_state['role'] == 'client':
    #client interface
    st.subheader("Your Assigned Workouts")
    client_id = get_client_id_by_username(st.session_state['username'])
    assigned_workouts = get_assigned_workouts(client_id)
    for aw in assigned_workouts:
        st.write(f"Workout Plan: {aw[1]} (Assigned on {aw[3]})")
        exercises = get_exercises_for_workout_plan(aw[0])
        for ex in exercises:
            st.write(f"- Exercise: {ex[1]}, Sets: {ex[2]}, Reps: {ex[3]}, Weight: {ex[4]} lbs")
            #log workut
            if st.button(f"Log '{ex[1]}'"):
                sets_completed = st.number_input("Sets Completed", min_value=0)
                reps_completed = st.number_input("Reps Performed", min_value=0)
                weight_used = st.number_input("Weight Used (lbs)", min_value=0)
                if st.button("Submit Log"):
                    log_workout(client_id, ex[0], sets_completed, reps_completed, weight_used)
                    st.success("Workout logged successfully!")
    st.subheader("Your Workout History")
    logs = get_workout_logs(client_id)
    df_logs = pd.DataFrame(logs, columns=['Date', 'Exercise', 'Sets', 'Reps', 'Weight'])
    st.table(df_logs)
            

else:
    st.warning('Please log in to access the application.')
    
if st.sidebar.checkbox('Register'):
    st.subheader("User Registration")
    reg_username = st.text_input("Choose a Username")
    reg_name = st.text_input("Full Name")
    reg_password = st.text_input("Choose a Password", type='password')
    reg_role = st.selectbox("Role", ["trainer", "client"])
    if st.button("Register"):
        if reg_username and reg_name and reg_password:
            add_user(reg_username, reg_name, reg_password, reg_role)
            st.success("User registered successfully!")
        else:
            st.error("Please fill in all the fields.")

