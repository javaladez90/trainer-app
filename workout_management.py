import sqlite3
from database_utils import connect_db

def add_workout_plan(name, description):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO workout_plans (name, description)
                       VALUES (?, ?)
                       ''', (name, description))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding workout plan: {e}")
        return None
    finally:
        conn.close()
        
def add_exercise(workout_plan_id, name, sets, reps, weight):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO exercises (workout_plan_id, name, sets, reps, weight)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (workout_plan_id, name, sets, reps, weight))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding exercise: {e}")
    finally:
        conn.close()
        
def assign_workout_to_client(client_id, workout_plan_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO assigned_workouts (client_id, workout_plan_id, assigned_date)
                       VALUES (?, ?, CURRENT_DATE)
                       ''', (client_id, workout_plan_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error assigning workout: {e}")
    finally:
        conn.close()
        
def get_assigned_workouts(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       SELECT aw.id, wp.name, wp.description, aw.assigned_date
                       FROM assigned_workouts aw
                       JOIN workout_plans wp ON aw.workout_plan_id = wp.id
                       WHERE aw.client_id = ?
                       ''', (client_id,))
        workouts = cursor.fetchall()
        return workouts
    except sqlite3.Error as e:
        print(f"Error retrieving assigned workouts ")
        return []
    finally:
        conn.close()
        
def get_exercises_for_workout_plan(workout_plan_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       SELECT id, name, sets, reps, weight
                       FROM exercises
                       WHERE workout_plan_id = ?
                       ''', (workout_plan_id,))
        exercises = cursor.fetchall()
        return exercises
    except sqlite3.Error as e:
        print(f"Error retrieving exercises: {e}")
        return []
    finally:
        conn.close()
        
def log_workout(client_id, exercise_id, sets_completed, reps_completed, weight_used):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO workout_logs (client_id, exercise_id, date, sets_completed, reps_completed, weight_used)
                       VALUES (?, ?, CUREENT_DATE, ?, ?, ?)
                       ''', (client_id, exercise_id, sets_completed, reps_completed, weight_used))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging workout: {e}")
    finally:
        conn.close()
        
def get_workout_logs(client_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       SELECT wl.date, e.name, wl.sets_completed, wl.reps_completed, wl.weight_used
                       FROM workout_logs wl
                       JOIN exercises e ON wl.exercise_id = e.id
                       WHERE wl.client_id = ?
                       ORDER BY wl.date DESC
                       ''', (client_id,))
        logs = cursor.fetchall()
        return logs
    except sqlite3.Error as e:
        print(f"Error retrieving workout logs: {e}")
        return []
    finally:
        conn.close()