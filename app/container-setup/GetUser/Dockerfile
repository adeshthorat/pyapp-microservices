#Global argument for Python version
ARG PYTHON_VER="3.10-slim"

#Can be overridden at build time
FROM python:${PYTHON_VER}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY getuser.py .

EXPOSE 5002

CMD ["python", "getuser.py"]
