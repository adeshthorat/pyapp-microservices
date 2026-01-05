# Hi, I'm Adesh ! 👋

I'm a Devops Engineer , love to build and deploy.

I believe true learning comes from hands-on practice. Building environments from scratch and unraveling their complexities has been a key driver in my growth.

Each challenge deepens my understanding and fuels my passion for continuous learning and problem-solving .

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adesh-thorat-0b8a541a8/)

---

# UI :

![alt text](/docs/devops_project.png)

# 🚀 Cloud-Native Microservices Platform (GitOps-Driven)

This repository contains a **production-style, cloud-native microservices application** designed to demonstrate **real-world DevOps, Kubernetes, and GitOps practices**.

The project started as a simple local application and gradually evolved into a **fully containerized, Kubernetes-based microservices platform** with automated CI/CD, observability, and GitOps-driven deployments.

---

## 📌 Project Overview

The application follows a **microservices architecture** where each service is independently developed, built, deployed, and managed.

### Core Use Case

A simple **user management system** exposing APIs to:

- Create a user
- Fetch user details
- Delete a user

All services communicate with a shared MySQL database and are exposed via an NGINX-based frontend.

---

## 🧱 Architecture Overview

---

## 🛠️ Tech Stack

### Application

- **Python Flask** – Backend microservices
- **NGINX** – Frontend and request routing
- **MySQL** – Persistent database

### Containerization & Orchestration

- **Docker** – Image creation
- **Kubernetes** – Container orchestration
- **Init Containers** – Pre-flight DB connectivity checks

### CI/CD & GitOps

- **GitHub Actions** – Continuous Integration
- **Kustomize** – Manifest abstraction and image management
- **Argo CD** – Continuous Deployment (GitOps)

### Observability

- **Prometheus** – Metrics collection
- **Grafana** – Metrics visualization and dashboards

---

## 📂 Repository Structure

```plaintext
repo/
│├── src
    backend/
│   ├── CreateUser/
│   ├── DeleteUser/
│   ├── GetUser/
│   ├── mysql_data/
│   └── .env
│├──frontend/
│├──k8s/
│   ├── kustomization.yaml
│   ├── base/
│   │   ├── create-user-deployment.yaml
│   │   ├── delete-user-deployment.yaml
│   │   ├── get-user-deployment.yaml
│   │   ├── mysql-statefulset.yaml
│   │   ├── nginx-deployment.yaml
│├── .github/
│   └── workflows/
│       └── image-builder.yaml
        └── update-kustomize.yaml
│└── README.md
│└── .gitignore
```

---

## 🔄 CI/CD Workflow Explained

### 1️⃣ Continuous Integration (GitHub Actions)

- Triggered on source-code changes
- Builds Docker images for the affected service
- Tags images using Git commit SHA
- Pushes images to container registry
- Updates image tags in `kustomization.yaml`

### 2️⃣ GitOps Deployment (Argo CD)

- Argo CD continuously watches the Git repository
- Detects manifest updates
- Syncs desired state to Kubernetes automatically
- Ensures the cluster always matches Git

---

## ⚙️ Kubernetes Design Decisions

- **Independent Deployments** for each microservice  
  Enables isolated scaling and safer rollouts

- **StatefulSet for MySQL**

  - PersistentVolumeClaims ensure data persistence
  - Stable network identity for database pods

- **Init Containers**

  - Verify database availability before application startup
  - Prevent crash loops during cold starts

- **Kustomize**
  - Clean separation of base manifests
  - Centralized image version management

---

## 📈 Future Enhancements

- Argo Rollouts for canary or blue-green deployments
- Centralized logging (EFK / Loki)
- AI-assisted log analysis
- Multi-environment overlays (dev/stage/prod)

---
