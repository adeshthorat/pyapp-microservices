from flask import Flask, jsonify ,request
from flask_cors import CORS
import mysql.connector, os, time
from dotenv import load_dotenv
import logging


app = Flask(__name__)
CORS(app)
load_dotenv()

SERVICE_VERSION = "v1.0.0"
logger = logging.getLogger('getuser_service')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load DB config from environment
db_config = {
    'host': os.getenv('DB_HOST'), #App-DB both are in container use DB_HOST = mysql-db else DB_HOST = '127.0.0.1'
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
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

@app.route('/getuser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, city FROM users WHERE id = %s", (user_id,))
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
    app.run(host='0.0.0.0', port=5002)
