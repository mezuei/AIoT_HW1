import sqlite3, random
from datetime import datetime, timedelta

DB_PATH = "aiotdb.db"
conn = sqlite3.connect(DB_PATH)
conn.execute("""
    CREATE TABLE IF NOT EXISTS sensors (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL    NOT NULL,
        humidity    REAL    NOT NULL,
        time        TEXT    NOT NULL
    )
""")
for i in range(30):
    t = round(random.uniform(20.0, 35.0), 1)
    h = round(random.uniform(40.0, 80.0), 1)
    ts = (datetime.now() - timedelta(seconds=(29 - i) * 2)).strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("INSERT INTO sensors (temperature, humidity, time) VALUES (?,?,?)", (t, h, ts))
conn.commit()
conn.close()
print("Seeded 30 rows into aiotdb.db → sensors")
