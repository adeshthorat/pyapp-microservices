import requests
import json
import time

# ==== CONFIG ====
HOST_IP = input("Enter EC2 Public ip: ")
NODE_PORT = input("Enter svc Node port: ")
START_ID = int(input("Enter From id: "))
END_ID = int(input("Enter to id: "))
API_URL = f"http://{HOST_IP}:{NODE_PORT}/deleteuser"

SLEEP_BETWEEN = 0.2  # seconds between calls (optional throttle)

# ==== BULK DELETE ====
for i in range(START_ID, END_ID + 1):
    payload = {"id": i}
    try:
        response = requests.delete(API_URL, json=payload, timeout=5)
        status = response.status_code
        msg = response.json() if response.headers.get('Content-Type', '').startswith('application/json') else response.text
        print(f"[{i}] Deleted ID={i} | Status={status} | Msg={msg}")
    except Exception as e:
        print(f"[{i}] Failed to delete ID={i} | Error={e}")
    time.sleep(SLEEP_BETWEEN)
