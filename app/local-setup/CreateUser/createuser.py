from flask import Flask, request, jsonify
import mysql.connector, os, time

app = Flask(__name__)

# Load DB config from environment
db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'), #App-DB both are in container use DB_HOST = mysql-db else DB_HOST = '127.0.0.1'
    'user': os.getenv('DB_USER', 'myuser'),
    'password': os.getenv('DB_PASS', 'mypass'),
    'database': os.getenv('DB_NAME', 'userdb'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Wait for DB to become ready
for i in range(10):
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL database........")
            conn.close()
            break
    except Exception as e:
        print("⏳ Waiting for MySQL...", e)
        time.sleep(2)

@app.route('/createuser', methods=['PUT'])
def update_user():✅
    data = request.get_json()
    user_id = data['id']
    name = data['name']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
    conn.commit()
    


    cursor.close()
    conn.close()

    return jsonify({'message': f'Success !  {user_id} updated is userdb database !'})

@app.route('/testdb', methods=['GET']) # type: ignore
def test_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            conn.close()
            return jsonify({'message': 'Database connection successful ✅'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
