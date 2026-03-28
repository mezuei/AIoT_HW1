"""
sensor_generator.py
--------------------
Simulates a DHT11 sensor: generates temperature & humidity readings
every 2 seconds and inserts them into SQLite3 database aiotdb.db.

Run this script first (in a separate terminal), then launch Streamlit.

  python sensor_generator.py
"""

import sqlite3
import random
import time
from datetime import datetime

DB_PATH = "aiotdb.db"


def init_db():
    """Create the sensors table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL    NOT NULL,
            humidity    REAL    NOT NULL,
            time        TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()
    print(f"[DB] Initialized: {DB_PATH} → table 'sensors' ready.")


def simulate_dht11():
    """
    DHT11 ranges:
      Temperature: 0 – 50 °C  (resolution ±0.1 °C)
      Humidity   : 20 – 90 %RH (resolution ±1 %)
    """
    temperature = round(random.uniform(20.0, 35.0), 1)   # comfortable room range
    humidity    = round(random.uniform(40.0, 80.0), 1)
    return temperature, humidity


def insert_reading(temperature: float, humidity: float):
    conn = sqlite3.connect(DB_PATH)
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO sensors (temperature, humidity, time) VALUES (?, ?, ?)",
        (temperature, humidity, now),
    )
    conn.commit()
    conn.close()


def main():
    init_db()
    print("[Generator] Starting DHT11 simulation — inserting every 2 seconds.")
    print("            Press Ctrl+C to stop.\n")

    count = 0
    while True:
        temp, hum = simulate_dht11()
        insert_reading(temp, hum)
        count += 1
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] #{count:4d}  Temp={temp:5.1f}°C   Humidity={hum:5.1f}%")
        time.sleep(2)


if __name__ == "__main__":
    main()
