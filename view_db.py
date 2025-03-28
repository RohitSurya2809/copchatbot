import sqlite3

conn = sqlite3.connect('instance/users.db')
cursor = conn.cursor()

# Get table schema
print('Users Table Schema:')
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
schema = cursor.fetchone()
if schema:
    print(schema[0])

# Get table content
print('\nUsers Table Content:')
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
if rows:
    print('\nID | Username | Password Hash | Created At')
    print('-' * 80)
    for row in rows:
        print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]}')
else:
    print('No users found in the database.')

conn.close()
