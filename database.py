import sqlite3
conn=sqlite3.connect("ats.db")
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               phone TEXT,
               email TEXT,
               degree TEXT,
               domain TEXT,
               skills TEXT,
               score TEXT,
               status TEXT
               )
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT UNIQUE,
               password TEXT
)
""")
cursor.execute("""
INSERT OR IGNORE INTO companies(
               email,
               password
               )
            VALUES(
               'admin@company.com',
               '123456'
               )
               """)
conn.commit()
conn.close()
print("Database Created Successfully")