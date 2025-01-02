import sqlite3
import hashlib

# SQLite Database Setup
def setup_user_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

setup_user_database()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        connection.commit()
        return "Registration successful! Please log in."
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        connection.close()

def login_user(username, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    return False
