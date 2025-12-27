from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector, os, time

app = Flask(__name__)
CORS(app)

SERVICE_VERSION = "v1.0.0"

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

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
                'message': f'No user found with ID {user_id}.',
                "service": "deleteuser",
                "version": SERVICE_VERSION,
                "status": "not_found"
                }), 404
        return jsonify({
            'message': f'Success ✅! User id {user_id} deleted.',
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
