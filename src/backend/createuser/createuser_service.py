from flask import Flask, request, jsonify ,request
from flask_cors import CORS
import mysql.connector, os, time
from dotenv import load_dotenv
import logging

app = Flask(__name__)
CORS(app)
load_dotenv()

SERVICE_VERSION = "v1.1.1"
logger = logging.getLogger('createuser_service')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load DB config from environment
db_config = {
    'host': os.getenv('DB_HOST'), #App-DB both are in container use DB_HOST = mysql-db else DB_HOST = '127.0.0.1'
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection(retries=3, delay=2):
    for attempt in range(1, retries+1):
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                return conn
        except Exception as e:
            print(f"DB connect attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    raise ConnectionError("❌Cannot connect to MySQL after retries")

@app.before_request
def log_request():
    logger.info(
        "Incoming request | method=%s path=%s remote_addr=%s",
        request.method,
        request.path,
        request.remote_addr
    )

@app.route('/createuser', methods=['PUT'])
def create_user():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({'error': 'Request JSON body required'}), 400
        user_id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        city = data.get('city')

        if user_id is None or name is None:
            return jsonify({'error': '`id` and `name` are required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (id, name, email, city) VALUES (%s, %s, %s, %s)",
                (int(user_id), name, email, city)
            )
            conn.commit()
            status = 201
            msg = f'Success ✅ ,New User {user_id} inserted in Database.'
        except mysql.connector.IntegrityError:
            # if id exists, do an update (mirror a simple upsert)
            cursor.execute(
                "UPDATE users SET name=%s, email=%s, city=%s WHERE id=%s",
                (name, email, city, int(user_id))
            )
            conn.commit()
            status = 200
            msg = f'Success ✅!{user_id} updated in Database !'
        finally:
            cursor.close()
            conn.close()

        return jsonify({
            'message': msg,
            'status': 'success',
            'status_code': status,
            'service': 'createuser',
            'version': SERVICE_VERSION
            }), 200

    except ConnectionError as ce:
        return jsonify({'error': str(ce)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Healthy🆗"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"message": "Database connection successful ✅"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
