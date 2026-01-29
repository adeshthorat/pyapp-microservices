# Application Code Updates Required

The production-grade configurations include health probes that require code changes in your Flask applications.

## Required Endpoints

Add the following endpoints to each Flask service:

### 1. CreateUser Service (`src/backend/CreateUser/app.py`)

```python
from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

# Existing endpoints...

@app.route('/health', methods=['GET'])
def health():
    """Liveness probe - returns 200 if app is alive"""
    return jsonify({"status": "healthy"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe - returns 200 if app can serve traffic"""
    try:
        # Test database connectivity
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306)),
            connect_timeout=5
        )
        connection.close()
        return jsonify({"status": "ready", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503
```

### 2. GetUser Service (`src/backend/GetUser/app.py`)

Add the same `/health` and `/ready` endpoints.

### 3. DeleteUser Service (`src/backend/DeleteUser/app.py`)

Add the same `/health` and `/ready` endpoints.

## Optional: Prometheus Metrics

For enhanced observability, add Prometheus metrics:

```python
pip install prometheus-flask-exporter
```

```python
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# This automatically exposes /metrics endpoint
# Tracks request count, duration, and more
```

## Updated Dockerfile Considerations

If using `readOnlyRootFilesystem: true`, ensure your containers can write to mounted volumes:

```dockerfile
# Example Dockerfile adjustments
FROM python:3.9-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Change ownership
RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
```

## Testing Health Endpoints Locally

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test readiness endpoint
curl http://localhost:5000/ready

# Expected responses:
# {"status": "healthy"}
# {"status": "ready", "database": "connected"}
```

## Note

These endpoints are **required** for the production deployments to work properly with the configured health probes. Without them, pods will fail liveness/readiness checks and may not start correctly.
