import mysql.connector, time, os

DB_HOST = os.getenv('DB_HOST', '127.0.0.1') #App-DB both are in container use DB_HOST = mysql-db else DB_HOST = '127.0.0.1'
DB_USER = os.getenv('DB_USER', 'myuser')
DB_PASS = os.getenv('DB_PASS', 'mypass')
DB_NAME = os.getenv('DB_NAME', 'userdb')
DB_PORT = int(os.getenv('DB_PORT', 3306))

print(f"🔍 Trying to connect to {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

for i in range(10):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT
        )
        if conn.is_connected():
            print("✅ Successfully connected to MySQL!")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            print("Connected to DB:", cursor.fetchone()[0])
            cursor.close()
            conn.close()
            break
    except Exception as e:
        print(f"⏳ Attempt {i+1}/10 failed:", e)
        time.sleep(5)
else:
    print("❌ Could not connect after several attempts.")
