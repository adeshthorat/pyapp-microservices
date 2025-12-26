from dotenv import load_dotenv
import os

load_dotenv()

print(f"Loaded DB host: {os.getenv('DB_HOST')}")