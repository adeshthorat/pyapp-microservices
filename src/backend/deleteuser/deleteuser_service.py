from flask import Flask, jsonify , request
from flask_cors import CORS
import mysql.connector, os, time
import logging

app = Flask(__name__)
CORS(app)

SERVICE_VERSION = "v1.1.0"
logger = logging.getLogger('createuser_service')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

for i in range(3):
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL database.......")
            conn.close()
            break
    except Exception as e:
        print("⏳ Waiting for MySQL...", e)
        time.sleep(3)

def get_db_connection(retries=8, delay=2):
    for attempt in range(1, retries+1):
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                return conn
        except Exception as e:
            print(f"DB connect attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    raise ConnectionError("Cannot connect to MySQL after retries")
@app.before_request
def log_request():
    logger.info(
        "Incoming request | method=%s path=%s remote_addr=%s",
        request.method,
        request.path,
        request.remote_addr
    )

@app.route('/deleteuser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        rows = cursor.rowcount
        cursor.close()
        conn.close()

        if rows == 0:
         return jsonify({
                'message': f'No user found with ID: {user_id}.',
                "service": "deleteuser",
                "version": SERVICE_VERSION,
                "status": "not_found"
                }), 404
        return jsonify({
            'message': f'Success ✅! User id: {user_id} deleted.',
            "service": "deleteuser",
            "version": SERVICE_VERSION,
            "status": "success✅"
            }), 200

    except ConnectionError as ce:
        return jsonify({'error': str(ce)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testdb', methods=['GET'])
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'message': 'Database connection successful ✅'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
