#Global argument for Python version
ARG PYTHON_VER="3.10-slim"

#Can be overridden at build time
FROM python:${PYTHON_VER}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY deleteuser.py .

EXPOSE 5001

CMD ["python", "deleteuser.py"]
