import sqlite3
from datetime import datetime
import os

DB_NAME = "bmi_data.db"

def get_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            date TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_record(name, weight, height, bmi, category):
    """
    Adds a new BMI record to the database.
    
    Args:
        name (str): User's name.
        weight (float): Weight in kg.
        height (float): Height in m.
        bmi (float): Calculated BMI.
        category (str): BMI Category.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO bmi_records (user_name, date, weight, height, bmi, category)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, current_date, weight, height, bmi, category))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def get_user_history(name):
    """
    Retrieves all records for a specific user, ordered by date.
    
    Args:
        name (str): The user's name to filter by.
        
    Returns:
        list of tuples: Records matching the user (date, bmi).
    """
    records = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, bmi FROM bmi_records 
            WHERE user_name = ? 
            ORDER BY date ASC
        ''', (name,))
        records = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database retrieval error: {e}")
    finally:
        if conn:
            conn.close()
    return records
