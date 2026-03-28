import time
import random
import requests
import json
import sys

FLASK_URL = "http://localhost:5000/sensor"

def simulate_sensor():
    print(f"Starting ESP32 Simulator. Sending data to {FLASK_URL} every 5 seconds...")
    while True:
        data = {
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2),
            "device_id": "ESP32_Test_Unit",
            "wifi_ssid": "AIoT_Network_1"
        }
        try:
            response = requests.post(FLASK_URL, json=data, timeout=5)
            print(f"Sent: {data} -> Response: {response.status_code} {response.text.strip()}")
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            
        time.sleep(5)

if __name__ == '__main__':
    simulate_sensor()
