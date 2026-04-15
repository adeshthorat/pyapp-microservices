# Blue-Green Deployment - Quick Reference

## 🎯 What You Get

Complete blue-green deployment setup for **all 4 services**:
- ✅ CreateUser
- ✅ GetUser  
- ✅ DeleteUser
- ✅ Frontend

## 📁 Files Created

```
k8s/rollouts/
├── BLUE_GREEN_GUIDE.md           ← Complete implementation guide
├── README.md                      ← Quick commands reference
├── analysis-template.yaml         ← Prometheus-based validation
├── createuser-rollout.yaml        ← Blue-green for createuser
├── getuser-rollout.yaml           ← Blue-green for getuser
├── deleteuser-rollout.yaml        ← Blue-green for deleteuser
└── frontend-rollout.yaml          ← Blue-green for frontend
```

## ⚡ Quick Start

### 1. Install Argo Rollouts
```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

### 2. Deploy Analysis Template
```bash
kubectl apply -f k8s/rollouts/analysis-template.yaml
```

### 3. Convert One Service (Start Small)
```bash
# Test with createuser first
kubectl delete deployment createuser-app
kubectl apply -f k8s/rollouts/createuser-rollout.yaml
```

### 4. Deploy New Version
```bash
kubectl argo rollouts set image createuser-rollout \
  createuser=adesh0303/eks-app:createuser-v2
```

### 5. Test Preview
```bash
kubectl port-forward svc/createuser-preview 5001:5000
curl http://localhost:5001/health
```

### 6. Promote
```bash
kubectl argo rollouts promote createuser-rollout
```

## 🔄 Workflow

![Blue-Green Workflow](blue_green_workflow.webp)

1. **Deploy Green** (new version) alongside Blue (current)
2. **Validate** Green using analysis + manual testing
3. **Switch** traffic from Blue → Green instantly
4. **Cleanup** old Blue version

## 📖 Documentation

- **Complete guide**: [`BLUE_GREEN_GUIDE.md`](file:///d:/pyapp-microservices/k8s/rollouts/BLUE_GREEN_GUIDE.md)
- **Quick commands**: [`README.md`](file:///d:/pyapp-microservices/k8s/rollouts/README.md)

## ✨ Key Benefits

- **Zero downtime** - Instant traffic switch
- **Easy rollback** - Just switch back to blue
- **Production testing** - Validate before going live
- **Automated validation** - Prometheus metrics analysis

## 🚨 Important Notes

1. **Requires Argo Rollouts** installation (one-time setup)
2. **Cannot coexist** with standard Deployments - delete Deployment before applying Rollout
3. **Preview services** created automatically for testing
4. **Manual promotion** required by default (set `autoPromotionEnabled: true` for auto)

## 🎓 Learn More

See Argo Rollouts docs: https://argoproj.github.io/argo-rollouts/
