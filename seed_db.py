import sqlite3
import random
import datetime
import os

DB_FILE = "aiotdb2.db"

# Start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
c.execute('''
    CREATE TABLE sensors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        device_id TEXT,
        wifi_ssid TEXT,
        timestamp DATETIME
    )
''')

now = datetime.datetime.now()
for i in range(50):
    # Each record 5 seconds apart, oldest first
    ts = now - datetime.timedelta(seconds=(50 - i) * 5)
    c.execute(
        "INSERT INTO sensors (temperature, humidity, device_id, wifi_ssid, timestamp) VALUES (?, ?, ?, ?, ?)",
        (
            round(random.uniform(20.0, 35.0), 2),
            round(random.uniform(40.0, 80.0), 2),
            "ESP32_Simulated",
            "AIoT_Network_1",
            ts.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

conn.commit()
conn.close()
print(f"Done! 50 records with proper timestamps written to {DB_FILE}")
