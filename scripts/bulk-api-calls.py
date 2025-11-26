import requests
import random
import string


# HOST_IP = input("Enter EC2 Public ip: ")
# NODE_PORT = input("Enter svc Node port: ")

API_URL = f"http://127.0.0.1:5000/createuser"

def random_name():
    return ''.join(random.choices(string.ascii_letters, k=6))

def random_email():
        return ''.join(random.choices(string.ascii_lowercase, k=6))

def random_city():
        return ''.join(random.choices(string.ascii_lowercase, k=4))



print(random_name())

print(f"{random_email()}@gmail.com")
print(random_city())





for i in range(150, 200):
    user_id = 1 + i
    name = random_name()
    email = f"{random_email()}@gmail.com"
    city = random_city()
    payload = { "id": user_id, "name": name,"email": email , "city": city }


    try:
        response = requests.put(API_URL, json=payload, timeout=5)
        print(f"[{i}] ID={user_id}, Name={name}, Status={response.status_code}, Msg={response.json()}")
    except Exception as e:
        print(f"[{i}] Failed: {e}")



