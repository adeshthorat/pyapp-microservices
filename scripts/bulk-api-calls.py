import requests
import random
import string

API_URL = "http://localhost:5000/createuser"

def random_name():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

for i in range(1, 1000):
    user_id = 3000 + i
    name = random_name()
    payload = {"id": user_id, "name": name}

    try:
        response = requests.put(API_URL, json=payload, timeout=5)
        print(f"[{i}] ID={user_id}, Name={name}, Status={response.status_code}, Msg={response.json()}")
    except Exception as e:
        print(f"[{i}] Failed: {e}")



