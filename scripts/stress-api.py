import requests
import random
import string

def show_intro():
    print("\033[1;34m" + "=" * 60 + "\033[0m")
    print("""\033[1;32mThis Script will call the following API services:\033[0m\n
        http://<node_external_ip>:<node_port>/createuser
        Payload: {"id": 5871, "name": "TFfvhj"}\n
        http://<node_external_ip>:<node_port>/deleteuser
        Payload: {"id": 5871}\n
        http://<node_external_ip>:<node_port>/getuser
        Payload: {"id": 5871}\n
        /testdb      →  Tests DB connectivity\n""")

    print("\033[1;34m" + "=" * 60 + "\033[0m")
    print("\033[1;33mSelect API to call:\033[0m\n")
    print("1️⃣. /createuser")
    print("2️⃣. /getuser")
    print("3️⃣. /deleteuser")
    print("4️⃣. /testdb")
    print("\033[1;34m" + "=" * 60 + "\033[0m\n")

def create_user():
    node_port = input("Enter NodePort: ").strip()
    FROM = int(input("Enter starting ID: "))
    TO = int(input("Enter ending ID:"))
    API_URL = f'{node_url}:{node_port}/createuser'


    for user_id in range(FROM, TO + 1):

        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        payload = {"id": user_id, "name": name}

        try:
            response = requests.put(API_URL, json=payload, timeout=5)
            print(f"[{user_id}] ID={user_id}, Name={name}, Status={response.status_code}, Msg={response.json()}")
        except Exception as e:
            print(f"[{user_id}] Failed: {e}")

def delete_user():
    node_port = input("Enter NodePort: ").strip()
    FROM = int(input("Enter starting ID: "))
    TO = int(input("Enter ending ID:"))
    API_URL = f'{node_url}:{node_port}/deleteuser/'

    for user_id in range(FROM, TO + 1):
        try:
            response = requests.delete(f"{API_URL}{user_id}", timeout=5)
            print(f"[{user_id}] ID={user_id},Status={response.status_code}, Msg={response.json()}")
        except Exception as e:
            print(f"[{user_id}] Failed: {e}")

def get_user():

    node_port = input("Enter NodePort: ").strip()
    FROM = int(input("Enter starting ID: "))
    TO = int(input("Enter ending ID:"))
    API_URL = f'{node_url}:{node_port}/getuser/'


    for user_id in range(FROM, TO + 1):
        try:
            response = requests.get(f"{API_URL}{user_id}", timeout=5)
            print(f"User id = [{user_id}] , Name ={response.json()}, Status={response.status_code}")
        except Exception as e:
            print(f"[{user_id}] Failed: {e}")

def test_db_connection():
    try:
        i = 0
        while i < 3:
            node_port = input("Enter NodePort: ").strip()
            API_URL = f'{node_url}:{node_port}/testdb'
            response = requests.get(f"{API_URL}", timeout=5)
            print(f"✅ DB Connection Working for {node_port}, Name ={response.json()}, Status={response.status_code}")
            i+=1
        exit(0)
    except Exception as e:
        print(f"❌ DB connection Failed : {e}")

def main():
    if CHOICE == '1':
        create_user()
    elif CHOICE == '2':
        get_user()
    elif CHOICE == '3':
        delete_user()
    elif CHOICE == '4':
        test_db_connection()
    else:
        print("Invalid Choice")

if __name__ == "__main__":
 show_intro()
 CHOICE = input("Enter Option: ", )
 node_ip = input("Enter Public Node ip: ").strip()
 node_url = f"http://{node_ip}"
 main()                