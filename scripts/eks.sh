#!/bin/bash

set -e

# -------- LOG FUNCTION --------
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# -------- INPUT VALIDATION --------
if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <cluster-name> <node-type> <node-count>"
  exit 1
fi

CLUSTER_NAME=$1
NODE_TYPE=$2
NODE_COUNT=$3

REGION="us-east-1"
NODEGROUP_NAME="${CLUSTER_NAME}-nodegroup"
SUBNETS="subnet-02af14a8e8cfdbed9,subnet-06630e707819975a9"

MIN_NODES=1
MAX_NODES=2

# -------- START --------
log "Starting EKS cluster creation"
log "Cluster Name: $CLUSTER_NAME"
log "Node Type: $NODE_TYPE"
log "Desired Nodes: $NODE_COUNT"

# -------- CREATE CLUSTER --------
log "Creating EKS cluster using eksctl..."

eksctl create cluster \
  --name "$CLUSTER_NAME" \
  --region "$REGION" \
  --nodegroup-name "$NODEGROUP_NAME" \
  --node-type "$NODE_TYPE" \
  --nodes "$NODE_COUNT" \
  --nodes-min "$MIN_NODES" \
  --nodes-max "$MAX_NODES" \
  --vpc-public-subnets "$SUBNETS"

log "Cluster creation initiated..."

# -------- VERIFY --------
log "Checking cluster status..."

aws eks describe-cluster \
  --name "$CLUSTER_NAME" \
  --region "$REGION" \
  --query "cluster.status" \
  --output text

# -------- UPDATE KUBECONFIG --------
log "Updating kubeconfig..."

aws eks update-kubeconfig \
  --region "$REGION" \
  --name "$CLUSTER_NAME"

log "Cluster setup complete ✅"

aws eks update-kubeconfig \
  --region "us-east-2" \
  --name "my-eks"