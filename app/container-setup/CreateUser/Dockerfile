FROM python:3.9 AS builder
COPY requirements.txt .
RUN pip install -r requirements.txt
FROM python:3.9-slim
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY . .
CMD ["python", "createuser.py"]