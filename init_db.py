import sqlite3
import os

# Ensure instance directory exists
os.makedirs('instance', exist_ok=True)

# Connect to database
conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print('Database initialized successfully!')
