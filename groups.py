import sqlite3
conn = sqlite3.connect('.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Vedomosti (
                    ID INTEGER PRIMARY KEY,
                    GroupID TEXT,
                    Column1 TEXT,
                    Column2 TEXT
                )''')
conn.commit()
conn.close()