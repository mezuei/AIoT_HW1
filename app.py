import sqlite3
import datetime
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DB_FILE = "aiotdb.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            device_id TEXT,
            wifi_ssid TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/sensor', methods=['POST'])
def receive_data():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        device_id = data.get('device_id', 'ESP32_Unknown')
        wifi_ssid = data.get('wifi_ssid', 'Unknown_Network')
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensors (temperature, humidity, device_id, wifi_ssid)
            VALUES (?, ?, ?, ?)
        ''', (temperature, humidity, device_id, wifi_ssid))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Data inserted"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    # Run the server on port 5000
    app.run(host='0.0.0.0', port=5000)
