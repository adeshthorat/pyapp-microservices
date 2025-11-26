from dotenv import load_dotenv
import os

load_dotenv()

print(f"Loaded DB host: {os.getenv('DB_HOST')}")


def random_name():
    return ''.join(random.choices(string.ascii_letters, k=6))

def random_email():
        return ''.join(f"{random.choices(string.ascii_lowercase, k=6)}.{random.choices(string.digits, k=3)}@gmail.com")

def random_city():
        return ''.join(random.choices(string.ascii_lowercase, k=4))



print(random_name())

