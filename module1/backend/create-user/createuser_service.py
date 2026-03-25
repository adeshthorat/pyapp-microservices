from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time
import logging
from typing import Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

SERVICE_VERSION = "v1.1.1"
SERVICE_NAME = "createuser_service"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(SERVICE_NAME)

# DB Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection(retries: int = 3, delay: int = 2) -> Optional[mysql.connector.MySQLConnection]:
    """Establishes a connection to the MySQL database with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                return conn
        except mysql.connector.Error as err:
            logger.warning(f"DB connection attempt {attempt}/{retries} failed: {err}")
            if attempt < retries:
                time.sleep(delay)
    
    logger.error("Failed to connect to MySQL after all retries.")
    raise ConnectionError("Cannot connect to MySQL database")

@app.before_request
def log_request_info():
    """Logs details of incoming requests."""
    logger.info(
        "Incoming request | method=%s path=%s remote_addr=%s",
        request.method,
        request.path,
        request.remote_addr
    )

@app.route('/createuser', methods=['PUT'])
def create_user():
    """Endpoint to create or update a user."""
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

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Use a more explicit upsert pattern
            insert_query = "INSERT INTO users (id, name, email, city) VALUES (%s, %s, %s, %s)"
            update_query = "UPDATE users SET name=%s, email=%s, city=%s WHERE id=%s"
            
            try:
                cursor.execute(insert_query, (int(user_id), name, email, city))
                conn.commit()
                status_code = 201
                msg = f'Success: New User {user_id} inserted.'
            except mysql.connector.IntegrityError:
                # Mirroring the simple upsert logic if ID exists
                cursor.execute(update_query, (name, email, city, int(user_id)))
                conn.commit()
                status_code = 200
                msg = f'Success: User {user_id} updated.'
            
            return jsonify({
                'message': msg,
                'status': 'success',
                'status_code': status_code,
                'service': 'createuser',
                'version': SERVICE_VERSION
            }), 200

        except mysql.connector.Error as db_err:
            logger.error(f"Database error: {db_err}")
            return jsonify({'error': 'Database operation failed'}), 500
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    except ConnectionError as ce:
        return jsonify({'error': str(ce)}), 503
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Basic health check endpoint."""
    return jsonify({"status": "Healthy", "version": SERVICE_VERSION}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Check readiness by verifying database connectivity."""
    try:
        conn = get_db_connection(retries=1)
        conn.close()
        return jsonify({"message": "Database connection successful", "status": "ready"}), 200
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({"status": "not ready", "error": "Database unreachable"}), 503

if __name__ == '__main__':
    # Running in debug false for "production-grade" feel, using environment for port/host if needed
    port = int(os.getenv('SERVICE_PORT', 5000))
    app.run(host='0.0.0.0', port=port)

