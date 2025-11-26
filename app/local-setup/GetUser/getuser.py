from flask import Flask, jsonify
import mysql.connector, os, time

app = Flask(__name__)

# Load DB config from environment
db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'myuser'),
    'password': os.getenv('DB_PASS', 'mypass'),
    'database': os.getenv('DB_NAME', 'userdb'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Wait for DB to be ready
for i in range(3):
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL database.")
            conn.close()
            break
    except Exception as e:
        print("⏳ Waiting for MySQL...", e)
        time.sleep(5)

@app.route('/getuser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({'message': f'User with ID {user_id} not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testdb', methods=['GET']) #type: ignore
def test_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            conn.close()
            return jsonify({'message': 'Database connection successful ✅'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
