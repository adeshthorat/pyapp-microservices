from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
import time
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

SERVICE_VERSION = "v1.1.3"
SERVICE_NAME = "getuser_service"

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

@app.route('/getuser/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """Endpoint to retrieve a user by ID."""
    try:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id, name, email, city FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                return jsonify({
                    "data": user,
                    "service": "getuser",
                    "version": SERVICE_VERSION,
                    "status": "success"
                }), 200

            return jsonify({
                "service": "getuser",
                "version": SERVICE_VERSION,
                "status": "error",
                "message": f"User with ID {user_id} not found"
            }), 404

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
    port = int(os.getenv('SERVICE_PORT', 5000))
    app.run(host='0.0.0.0', port=port)

