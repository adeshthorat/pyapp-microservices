ARG PYTHON_VER="3.10-slim"
#Can be overridden at build time
FROM python:${PYTHON_VER}
LABEL maintainer="adeshthorat"
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache