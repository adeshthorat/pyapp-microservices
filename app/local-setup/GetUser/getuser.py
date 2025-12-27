from flask import Flask, jsonify , request , g
import mysql.connector, os, time
import logging

app = Flask(__name__)

SERVICE_VERSION = "v1.0.1"
logger = logging.getLogger('getuser_service')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Load DB config from environment
db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'myuser'),
    'password': os.getenv('DB_PASS', 'mypass'),
    'database': os.getenv('DB_NAME', 'userdb'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Wait for DB to be ready
for i in range(10):
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL database.")
            conn.close()
            break
    except Exception as e:
        print("⏳ Waiting for MySQL...", e)
        time.sleep(5)

@app.before_request
def log_request():
    logger.info(
        "Incoming request | method=%s path=%s remote_addr=%s",
        request.method,
        request.path,
        request.remote_addr
    )
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
            return jsonify({
                "data": user,
                "service": "getuser",
                "version": SERVICE_VERSION,
                "status": "success✅"                
            }), 200
        return jsonify({
            "service": "getuser",
            "version": SERVICE_VERSION,
            "status": "error",
            "message": f"User with ID {user_id} not found❎"
        }), 404
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
