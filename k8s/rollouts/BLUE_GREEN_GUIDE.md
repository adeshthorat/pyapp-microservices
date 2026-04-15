# Blue-Green Deployment Implementation Guide

## 🎯 What is Blue-Green Deployment?

Blue-green deployment is a release strategy where you run two identical production environments:
- **Blue** (current/stable version) - Serving live traffic
- **Green** (new version) - Being tested/validated

### How It Works

```
Step 1: Blue serving 100% traffic
┌─────────────┐
│   Blue v1   │ ◄─── 100% traffic
└─────────────┘

Step 2: Deploy Green (new version)
┌─────────────┐     ┌─────────────┐
│   Blue v1   │     │  Green v2   │
└─────────────┘     └─────────────┘
      ▲                    
      │                    
   100% traffic         (testing/validation)

Step 3: Switch traffic to Green
┌─────────────┐     ┌─────────────┐
│   Blue v1   │     │  Green v2   │ ◄─── 100% traffic
└─────────────┘     └─────────────┘

Step 4: Cleanup old Blue
                    ┌─────────────┐
                    │  Green v2   │ ◄─── 100% traffic
                    └─────────────┘
```

### Benefits
- ✅ **Zero downtime** - instant traffic switch
- ✅ **Easy rollback** - just switch back to blue
- ✅ **Testing in production** - validate before switching traffic
- ✅ **Automated validation** - metrics-based promotion

---

## 📋 Prerequisites

### 1. Install Argo Rollouts

```bash
# Create namespace
kubectl create namespace argo-rollouts

# Install Argo Rollouts controller
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml

# Verify installation
kubectl get pods -n argo-rollouts

# Install kubectl plugin (optional but recommended)
# For Windows PowerShell:
# Download from https://github.com/argoproj/argo-rollouts/releases/latest
# Or use: kubectl argo rollouts version
```

### 2. Update Your Application Code

Add health endpoints to your Flask services (required for analysis):

```python
@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

@app.route('/ready', methods=['GET'])  
def ready():
    # Test DB connection
    return {"status": "ready"}, 200
```

See [`APP_CODE_UPDATES.md`](file:///d:/pyapp-microservices/APP_CODE_UPDATES.md) for complete code.

---

## 🚀 Implementation Steps

### Step 1: Deploy Analysis Template

This defines how to validate the new version:

```bash
kubectl apply -f k8s/rollouts/analysis-template.yaml
```

### Step 2: Convert Deployments to Rollouts

I'll create rollouts for all services. You'll replace standard Deployments with Rollouts.

**For CreateUser service:**

```bash
# Delete existing deployment
kubectl delete deployment createuser-app

# Deploy rollout
kubectl apply -f k8s/rollouts/createuser-rollout.yaml

# Verify
kubectl get rollout createuser-rollout
```

**Repeat for other services using the rollout files I'll create below.**

### Step 3: Deploy a New Version

When you want to deploy a new version:

```bash
# Update image in rollout YAML or use kubectl
kubectl argo rollouts set image createuser-rollout \
  createuser=adesh0303/eks-app:createuser-v2

# Watch the rollout progress
kubectl argo rollouts get rollout createuser-rollout --watch
```

**What happens:**
1. ✅ Green version (v2) starts alongside Blue (v1)
2. ✅ Analysis runs (checks success rate, latency from Prometheus)
3. ⏸️ Rollout **pauses** waiting for manual promotion
4. ✅ You can test Green version via preview service

### Step 4: Test the Green Version

```bash
# Access preview service (before switching traffic)
kubectl port-forward svc/createuser-preview 5001:5000

# Test in another terminal
curl http://localhost:5001/health
curl http://localhost:5001/createuser -X POST -d '{"name":"test"}'
```

### Step 5: Promote or Abort

**If tests pass - Promote:**
```bash
kubectl argo rollouts promote createuser-rollout
```

**If tests fail - Abort:**
```bash
kubectl argo rollouts abort createuser-rollout
# Rollback to previous version
kubectl argo rollouts undo createuser-rollout
```

### Step 6: Monitor

```bash
# Watch rollout status
kubectl argo rollouts get rollout createuser-rollout --watch

# View history
kubectl argo rollouts history createuser-rollout

# Check analysis results
kubectl get analysisrun
```

---

## 🎨 Visualization

Use Argo Rollouts Dashboard (optional):

```bash
kubectl argo rollouts dashboard
# Opens http://localhost:3100
```

Or use Kiali (if Istio installed):
```bash
istioctl dashboard kiali
```

---

## 🔄 Complete Workflow Example

### Scenario: Deploy CreateUser v2

```bash
# 1. Check current status
kubectl argo rollouts get rollout createuser-rollout
# Shows: Stable version running

# 2. Update to new version
kubectl argo rollouts set image createuser-rollout \
  createuser=adesh0303/eks-app:createuser-v2

# 3. Watch deployment
kubectl argo rollouts get rollout createuser-rollout --watch
# Output shows:
# - Green pods starting
# - Analysis running
# - Status: Paused (waiting for promotion)

# 4. Test preview service
kubectl get svc createuser-preview
kubectl port-forward svc/createuser-preview 5001:5000
curl http://localhost:5001/health

# 5. Check analysis results
kubectl get analysisrun -l rollout=createuser-rollout
# Shows success-rate, latency metrics

# 6. Promote if successful
kubectl argo rollouts promote createuser-rollout

# 7. Verify traffic switched
kubectl argo rollouts get rollout createuser-rollout
# Shows: 100% traffic to new version
```

---

## ⚙️ Configuration Options

### Auto-Promotion (No Manual Approval)

Edit rollout YAML:
```yaml
strategy:
  blueGreen:
    autoPromotionEnabled: true  # Changed from false
```

### Adjust Analysis Criteria

Edit `analysis-template.yaml`:
```yaml
metrics:
  - name: success-rate
    successCondition: result[0] >= 0.95  # 95% success rate
  - name: avg-response-time
    successCondition: result[0] <= 500   # 500ms max latency
```

### Canary Instead of Blue-Green

For gradual traffic shifting (e.g., 10% → 50% → 100%):

```yaml
strategy:
  canary:
    steps:
      - setWeight: 10
      - pause: {duration: 2m}
      - setWeight: 50
      - pause: {duration: 5m}
      - setWeight: 100
```

---

## 🚨 Rollback Procedures

### Automatic Rollback

If analysis fails, rollout automatically aborts and stays on blue version.

### Manual Rollback

```bash
# Abort current rollout
kubectl argo rollouts abort createuser-rollout

# Rollback to previous version
kubectl argo rollouts undo createuser-rollout

# Rollback to specific revision
kubectl argo rollouts undo createuser-rollout --to-revision=3
```

---

## 📊 Monitoring & Observability

### Key Metrics to Monitor

**Pre-Promotion:**
- Success rate (5xx errors)
- Latency (p95, p99)
- Resource usage

**Post-Promotion:**
- Traffic distribution
- Error rates
- User complaints

### Prometheus Queries

```promql
# Success rate
sum(rate(http_requests_total{status!~"5.."}[2m])) / sum(rate(http_requests_total[2m]))

# P95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[2m]))

# Error rate by version
rate(http_requests_total{status=~"5..", version="v2"}[2m])
```

---

## 🎯 Best Practices

1. **Always test preview service** before promoting
2. **Monitor metrics** during rollout
3. **Set realistic analysis thresholds** (don't expect 100% success)
4. **Keep rollback plan ready** 
5. **Use manual promotion** for critical services initially
6. **Automate later** once confident in analysis
7. **Document rollout procedures** for your team

---

## 🆚 Comparison: Standard vs Blue-Green

| Feature | Standard Deployment | Blue-Green Rollout |
|---------|-------------------|-------------------|
| Downtime | Brief (pod restart) | Zero downtime |
| Rollback speed | 30-60s | Instant (<5s) |
| Testing before switch | Limited | Full production test |
| Traffic control | RollingUpdate only | Instant 100% switch |
| Complexity | Simple | Requires Argo Rollouts |
| Resource usage | 1x | 2x during rollout |

---

## 🔗 Next Steps

1. Install Argo Rollouts
2. Add health endpoints to Flask apps
3. Test with one service first (createuser)
4. Monitor and validate
5. Roll out to other services
6. Consider automation with GitOps (ArgoCD + Argo Rollouts)

---

## 📝 Troubleshooting

**Issue: Rollout stuck in "Paused" state**
```bash
# Check analysis results
kubectl get analysisrun
kubectl describe analysisrun <name>

# Manually promote if analysis passed
kubectl argo rollouts promote createuser-rollout
```

**Issue: Analysis always fails**
```bash
# Check if Prometheus is accessible
kubectl get svc -n monitoring prometheus-server

# Verify metrics endpoint
kubectl port-forward svc/createuser 5000:5000
curl http://localhost:5000/metrics
```

**Issue: Pods not starting**
```bash
# Check pod events
kubectl describe rollout createuser-rollout
kubectl get pods -l app=createuser
kubectl describe pod <pod-name>
```

---

For complete Argo Rollouts documentation: https://argoproj.github.io/argo-rollouts/
