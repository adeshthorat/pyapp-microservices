#!/bin/bash
# Update system packages
sudo apt-get update -y

# Install prerequisites
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    git

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Enable and start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Add ec2-user (or ubuntu) to docker group
sudo usermod -aG docker $USER

# Install Docker Compose (latest stable release)
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest \
  | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

cd / && git clone --branch feature https://github.com/adeshthorat/pyapp-microservices.git

# Verify installations
docker --version
docker-compose --version
git --version
