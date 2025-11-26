# Hi, I'm Adesh ! 👋

I'm a Devops Engineer , love to build and deploy.

I believe true learning comes from hands-on practice. Building environments from scratch and unraveling their complexities has been a key driver in my growth.

Each challenge deepens my understanding and fuels my passion for continuous learning and problem-solving .

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adesh-thorat-0b8a541a8/)

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://kubernetes.io" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/kubernetes/kubernetes-icon.svg" alt="kubernetes" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>

---

# Flask Microservices with Docker

This project demonstrates a **3-Microservice Architecture** using **Flask**, **Docker**, and a **MySQL** database.  
Each microservice runs in its own isolated container and communicates with a shared database container over a custom Docker network.

**Flowchart**
![alt text](/img/flow.png)

🧩 Microservices Overview

1️⃣ CreateUser Service : Handles **user creation** and adds records to the MySQL database.

2️⃣ DeleteUser Service : Manages **user deletion** by removing user entries from the database.

3️⃣ GetUser Service : Retrieves **user information** based on the provided user ID.

---

## 🗄️ Database Configuration

- Image:`mysql:8.0-debian`
- Purpose: Centralized database for all microservices.
- Persistence:Data is stored persistently using Docker volumes.

## 📦 Docker Volume for Data Persistence

Database persistence is handled via Docker volume:

Host Path : /mysql

Container Path : /var/lib/mysql

This ensures data is retained even after container restarts.

## API Endpoints

1. CreateUser service:

curl -X PUT http://localhost:5000/createuser -H "Content-Type: application/json" -d '{"id":5122, "name":"Jane Doe"}'

---

2. DeleteUser Service

URL: http://localhost:5001/deleteuser/<user_id>
Method: DELETE

Example:

curl -X DELETE http://localhost:5001/deleteuser \
 -H "Content-Type: application/json" \
 -d '{"id":5122}'

---

3.GetUser Service

URL: http://localhost:5002/getuser
Method: POST

Example:

curl -X POST http://localhost:5002/getuser \
 -H "Content-Type: application/json" \
 -d '{"id":5122}'

---

🐳 Containerization Summary

1.  microservice is containerized separately
2.  Independent Dockerfiles per service
3.  Shared MySQL database container
4.  Connected through my-appnet

---

🚀 Testing Microservices in Bulk

You can automate or stress-test API calls using:

scripts/bulk-api-calls.py
This script sends multiple API requests across services for performance and integration testing.

## 📁 Project Structure

```plaintext
pyapp/
│├── app/container-setup/
│   ├── CreateUser/
│   ├── DeleteUser/
│   ├── GetUser/
│   ├── mysql_data/
│   └── .env
│├── scripts/
│   └── bulk-api-calls.py
│└── README.md
```
