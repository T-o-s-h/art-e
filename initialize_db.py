import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert a record
cursor.execute('''
INSERT INTO users (username, email) VALUES (?, ?)
''', ('user1', 'user1@example.com'))

# Commit the transaction
conn.commit()

# Query the database
cursor.execute('SELECT * FROM users')
print(cursor.fetchall())

# Close the connection
conn.close()
