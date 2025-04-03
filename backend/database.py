import sqlite3

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        security_question TEXT NOT NULL,
        security_answer TEXT NOT NULL
    )''')
    return conn
