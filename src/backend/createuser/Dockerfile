#Global argument for Python version
ARG PYTHON_VER="3.10-slim"

#Can be overridden at build time
FROM python:${PYTHON_VER}
LABEL app="CreateuserService"
LABEL maintainer="adeshthorat"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache

COPY createuser_service.py .

EXPOSE 5000

CMD ["python", "createuser_service.py"]

