# Production-Grade Kubernetes Deployment Guide

## Overview

This guide covers deploying the production-ready microservices platform with all security, networking, and reliability features.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Istio Gateway (HTTPS)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│         Frontend (NGINX) - ClusterIP Service                 │
│         - mTLS enabled                                       │
│         - Network Policies                                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │               │
┌───────▼──────┐ ┌────▼─────┐ ┌──────▼───────┐
│ CreateUser   │ │ GetUser  │ │ DeleteUser   │
│ Service      │ │ Service  │ │ Service      │
│ - HPA        │ │ - HPA    │ │ - HPA        │
│ - PDB        │ │ - PDB    │ │ - PDB        │
│ - Health     │ │ - Health │ │ - Health     │
└───────┬──────┘ └────┬─────┘ └──────┬───────┘
        └──────────────┼──────────────┘
                       │
            ┌──────────▼───────────┐
            │   MySQL StatefulSet  │
            │   - PVC Storage      │
            │   - Network Policy   │
            │   - Resource Limits  │
            └──────────────────────┘
```

## Deployment Steps

### Phase 1: Core Security (CRITICAL - Deploy First)

```bash
# 1. Create namespace with Pod Security Standards
kubectl apply -f k8s/pod-security-standards.yaml

# 2. Deploy secrets (UPDATE passwords before applying!)
kubectl apply -f k8s/secrets.yaml

# 3. Deploy non-sensitive config
kubectl apply -f k8s/config.yaml

# 4. Verify secrets created
kubectl get secrets pyapp-secrets -o yaml
```

### Phase 2: RBAC & Service Accounts

```bash
# Deploy service accounts and roles
kubectl apply -f k8s/rbac/service-accounts.yaml

# Verify
kubectl get serviceaccounts
kubectl get roles
kubectl get rolebindings
```

### Phase 3: Core Application Services

```bash
# Deploy using kustomize (without optional components)
kubectl apply -k k8s/

# Or deploy individually
kubectl apply -f k8s/mysqldb/
kubectl apply -f k8s/createuser/
kubectl apply -f k8s/getuser/
kubectl apply -f k8s/deleteuser/
kubectl apply -f k8s/frontend/

# Verify deployments
kubectl get deployments
kubectl get statefulsets
kubectl get services
kubectl get pods
```

### Phase 4: Network Policies (Zero-Trust)

```bash
# Deploy network policies
kubectl apply -f k8s/network-policies/

# Verify policies created
kubectl get networkpolicies

# Test connectivity (should succeed)
kubectl exec -it deployment/createuser-app -- curl http://mysqldb:3306

# Test unauthorized access (should fail)
kubectl run test --rm -it --image=busybox -- wget -O- http://mysqldb:3306
```

### Phase 5: Autoscaling & Reliability

```bash
# Deploy HPA (requires metrics-server)
kubectl apply -f k8s/hpa/backend-hpa.yaml

# Deploy PodDisruptionBudgets
kubectl apply -f k8s/pdb/all-services-pdb.yaml

# Verify HPA
kubectl get hpa -w

# Verify PDB
kubectl get pdb
```

### Phase 6: Istio Service Mesh (Optional)

**Prerequisites**: Install Istio first:

```bash
# Download and install Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y

# Enable sidecar injection for default namespace
kubectl label namespace default istio-injection=enabled
```

**Deploy Istio configs**:

```bash
# Deploy Istio resources
kubectl apply -f k8s/istio/gateway.yaml
kubectl apply -f k8s/istio/virtual-services.yaml
kubectl apply -f k8s/istio/destination-rules.yaml
kubectl apply -f k8s/istio/peer-authentication.yaml
kubectl apply -f k8s/istio/authorization-policies.yaml
kubectl apply -f k8s/istio/telemetry.yaml

# Restart pods to inject sidecars
kubectl rollout restart deployment/createuser-app
kubectl rollout restart deployment/getuser-app
kubectl rollout restart deployment/delete-app
kubectl rollout restart deployment/frontend-app

# Get Istio Gateway external IP
kubectl get svc istio-ingressgateway -n istio-system
```

**Access application**:
```bash
# Get external IP
export INGRESS_HOST=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Access application
curl http://$INGRESS_HOST/
```

### Phase 7: Argo Rollouts (Optional - Blue-Green Deployments)

**Prerequisites**: Install Argo Rollouts:

```bash
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
```

**Deploy Rollouts**:

```bash
# Deploy analysis template
kubectl apply -f k8s/rollouts/analysis-template.yaml

# Deploy rollout (replaces deployment)
kubectl delete deployment createuser-app
kubectl apply -f k8s/rollouts/createuser-rollout.yaml

# Monitor rollout
kubectl argo rollouts get rollout createuser-rollout --watch
```

## Verification

### Security Validation

```bash
# 1. Check Pod Security Standards
kubectl get pods -o json | jq '.items[].spec.securityContext'

# 2. Verify no privileged containers
kubectl get pods -o json | jq '.items[].spec.containers[] | select(.securityContext.privileged==true)'

# 3. Check resource limits
kubectl get pods -o json | jq '.items[].spec.containers[] | {name: .name, resources: .resources}'

# 4. Verify secrets (should not show plaintext)
kubectl get configmap pyapp-config -o yaml | grep -i pass
```

### Network Policy Testing

```bash
# Test authorized access (should work)
kubectl exec -it deployment/createuser-app -c createuser -- nc -zv mysqldb 3306

# Test unauthorized access (should be blocked)
kubectl run test-pod --rm -it --image=nicolaka/netshoot -- nc -zv mysqldb 3306
```

### Health & Availability

```bash
# Check health endpoints
kubectl port-forward svc/createuser 5000:5000
curl http://localhost:5000/health
curl http://localhost:5000/ready

# Monitor HPA scaling
kubectl get hpa -w

# Test PDB during node drain
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
# Should respect PDB and maintain minAvailable pods
```

### Istio Mesh Validation

```bash
# Check mTLS status
istioctl authn tls-check deployment/createuser-app.default

# Verify sidecars injected
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].name}' | grep istio-proxy

# Access Kiali dashboard
istioctl dashboard kiali

# Access Jaeger for distributed tracing
istioctl dashboard jaeger

# View Grafana metrics
istioctl dashboard grafana
```

## Monitoring

### Prometheus Queries

```promql
# Request rate by service
rate(istio_requests_total[5m])

# Error rate
rate(istio_requests_total{response_code=~"5.."}[5m])

# P95 latency
histogram_quantile(0.95, rate(istio_request_duration_milliseconds_bucket[5m]))

# Pod CPU usage
rate(container_cpu_usage_seconds_total[5m])

# Pod Memory usage
container_memory_working_set_bytes
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check security context issues
kubectl get events --sort-by='.lastTimestamp'

# Check if metrics-server is running (for HPA)
kubectl get deployment metrics-server -n kube-system
```

### Network Policy Issues

```bash
# Temporarily disable network policies for testing
kubectl delete networkpolicies --all

# Check network policy logs
kubectl describe networkpolicy <policy-name>
```

### Istio Issues

```bash
# Check sidecar injection
kubectl get namespace default -o jsonpath='{.metadata.labels.istio-injection}'

# Verify Istio installation
istioctl verify-install

# Check proxy status
istioctl proxy-status

# View proxy logs
kubectl logs <pod-name> -c istio-proxy
```

## Rollback Procedures

### Rollback Deployment

```bash
kubectl rollout undo deployment/createuser-app
kubectl rollout status deployment/createuser-app
```

### Rollback Argo Rollout

```bash
kubectl argo rollouts undo createuser-rollout
kubectl argo rollouts get rollout createuser-rollout --watch
```

### Disable Istio

```bash
# Remove istio-injection label
kubectl label namespace default istio-injection-

# Delete Istio configs
kubectl delete -f k8s/istio/

# Restart pods
kubectl rollout restart deployment --all
```

## Production Checklist

- [ ] Secrets encrypted at rest
- [ ] Pod Security Standards enforced
- [ ] All containers have resource limits
- [ ] All containers run as non-root
- [ ] Network policies applied
- [ ] Health probes configured
- [ ] HPA configured for autoscaling
- [ ] PDB configured for availability
- [ ] Monitoring & alerting configured
- [ ] Backup strategy for MySQL
- [ ] TLS certificates for HTTPS
- [ ] Log aggregation configured
- [ ] Disaster recovery plan documented

## Next Steps

1. **Add TLS to Istio Gateway** - Configure HTTPS with valid certificates
2. **Implement External Secrets** - Use AWS Secrets Manager, Vault, or Azure Key Vault
3. **Configure Log Aggregation** - Deploy EFK stack or use cloud logging
4. **Set up Alerting** - Configure Prometheus AlertManager
5. **Implement Backups** - Schedule MySQL backups to cloud storage
6. **Load Testing** - Use k6 or Locust to validate autoscaling
7. **Disaster Recovery** - Document and test DR procedures
