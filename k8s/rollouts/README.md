# Quick Deployment Script for Blue-Green Rollouts

## Step-by-Step Commands

### 1. Install Argo Rollouts (One-time setup)

```bash
# Create namespace
kubectl create namespace argo-rollouts

# Install controller
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Verify
kubectl get pods -n argo-rollouts
```

### 2. Deploy Analysis Templates

```bash
kubectl apply -f k8s/rollouts/analysis-template.yaml
```

### 3. Convert Services to Rollouts

**Option A: Deploy all rollouts at once**

```bash
# Delete existing deployments
kubectl delete deployment createuser-app
kubectl delete deployment getuser-app
kubectl delete deployment delete-app
kubectl delete deployment frontend-app

# Deploy all rollouts
kubectl apply -f k8s/rollouts/createuser-rollout.yaml
kubectl apply -f k8s/rollouts/getuser-rollout.yaml
kubectl apply -f k8s/rollouts/deleteuser-rollout.yaml
kubectl apply -f k8s/rollouts/frontend-rollout.yaml

# Verify
kubectl get rollouts
```

**Option B: Deploy one service at a time (recommended)**

```bash
# Start with createuser
kubectl delete deployment createuser-app
kubectl apply -f k8s/rollouts/createuser-rollout.yaml
kubectl get rollout createuser-rollout

# After validating, continue with others...
```

### 4. Deploy New Version

```bash
# Update image tag in rollout YAML or use kubectl
kubectl argo rollouts set image createuser-rollout \
  createuser=adesh0303/eks-app:createuser-v2

# Watch progress
kubectl argo rollouts get rollout createuser-rollout --watch
```

### 5. Test Preview Service

```bash
# Port-forward to preview service
kubectl port-forward svc/createuser-preview 5001:5000

# Test in another terminal
curl http://localhost:5001/health
curl http://localhost:5001/createuser -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"test","email":"test@example.com"}'
```

### 6. Promote or Abort

```bash
# If tests pass - promote to production
kubectl argo rollouts promote createuser-rollout

# If tests fail - abort and rollback
kubectl argo rollouts abort createuser-rollout
kubectl argo rollouts undo createuser-rollout
```

---

## Common Operations

### Check Rollout Status

```bash
# Get current status
kubectl argo rollouts status createuser-rollout

# Detailed view
kubectl argo rollouts get rollout createuser-rollout

# Watch live
kubectl argo rollouts get rollout createuser-rollout --watch
```

### View History

```bash
kubectl argo rollouts history createuser-rollout
```

### Rollback to Specific Version

```bash
kubectl argo rollouts undo createuser-rollout --to-revision=2
```

### Pause/Resume Rollout

```bash
# Pause
kubectl argo rollouts pause createuser-rollout

# Resume
kubectl argo rollouts resume createuser-rollout
```

---

## GitOps Integration (with ArgoCD)

If you're using ArgoCD, update your Application manifest:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: pyapp-microservices
spec:
  source:
    path: k8s
    repoURL: https://github.com/adeshthorat/pyapp-microservices
    targetRevision: main
  destination:
    namespace: default
    server: https://kubernetes.default.svc
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Then ArgoCD will automatically sync rollouts from Git!

---

## Monitoring Dashboard

```bash
# Start Argo Rollouts Dashboard
kubectl argo rollouts dashboard

# Access at http://localhost:3100
```

---

## Troubleshooting

**Rollout stuck at "Paused"**
```bash
kubectl get analysisrun
kubectl describe analysisrun <name>
# Check if metrics are available
```

**Can't promote**
```bash
# Make sure rollout is in "Paused" state
kubectl argo rollouts status createuser-rollout
```

**Analysis failing**
```bash
# Check Prometheus connectivity
kubectl port-forward -n monitoring svc/prometheus-server 9090:80
# Visit http://localhost:9090
```

---

See [`BLUE_GREEN_GUIDE.md`](file:///d:/pyapp-microservices/k8s/rollouts/BLUE_GREEN_GUIDE.md) for complete documentation.
