import sqlite3
import mysql.connector
from config import DB_CONFIG

def migrate_data():
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('../instance/users.db')
    sqlite_cursor = sqlite_conn.cursor()

    # Connect to MySQL database
    mysql_conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    mysql_cursor = mysql_conn.cursor()

    # Get all users from SQLite
    sqlite_cursor.execute('SELECT username, password_hash, created_at FROM users')
    users = sqlite_cursor.fetchall()

    # Insert users into MySQL
    for user in users:
        mysql_cursor.execute(
            'INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)',
            user
        )

    # Commit changes and close connections
    mysql_conn.commit()
    sqlite_cursor.close()
    sqlite_conn.close()
    mysql_cursor.close()
    mysql_conn.close()

    print('Data migration completed successfully!')

if __name__ == '__main__':
    migrate_data()
