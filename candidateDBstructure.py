import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('candidates.db')
cursor = conn.cursor()

# Modify the table schema to include an "approved" column
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        dob DATE,
        age INTEGER,
        skills TEXT,
        documents TEXT,  -- Store serialized documents as text
        approved INTEGER  -- 1 for approved, 0 for not approved
    )
''')
conn.commit()

# Close the database connection
conn.close()