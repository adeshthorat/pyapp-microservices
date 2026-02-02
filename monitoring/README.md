# Kubernetes Monitoring with Prometheus and Grafana

This directory contains the Kubernetes manifests for deploying Prometheus and Grafana monitoring stack on Minikube.

## Components Deployed

### Prometheus
- **Namespace**: `monitoring`
- **Service**: `prometheus-service` (NodePort: 30090)
- **Purpose**: Metrics collection and storage
- **Scrape Targets**:
  - Kubernetes API Server
  - Kubernetes Nodes (kubelet)
  - cAdvisor (container metrics)
  - Kubernetes Pods (with annotation `prometheus.io/scrape: "true"`)
  - Kubernetes Service Endpoints

### Grafana
- **Namespace**: `monitoring`
- **Service**: `grafana-service` (NodePort: 30030)
- **Purpose**: Metrics visualization and dashboards
- **Default Credentials**: 
  - Username: `admin`
  - Password: `admin` (you'll be prompted to change on first login)

### Kube-State-Metrics
- **Namespace**: `monitoring`
- **Service**: `kube-state-metrics`
- **Purpose**: Exposes cluster-level metrics about Kubernetes objects (pods, deployments, services, etc.)

## Accessing the Services

Since you're using Minikube with Docker driver, you need to use `minikube service` command to access the services:

### Access Prometheus
```powershell
minikube service prometheus-service -n monitoring
```

This will open Prometheus UI in your default browser. You can:
- Query metrics using PromQL
- View targets at `/targets` endpoint
- Check configuration at `/config` endpoint

### Access Grafana
```powershell
minikube service grafana-service -n monitoring
```

This will open Grafana UI in your default browser.

**First Login**:
1. Username: `admin`
2. Password: `admin`
3. You'll be prompted to change the password

**Pre-configured Dashboard**:
- Navigate to **Dashboards** → **Browse**
- Open **Kubernetes Cluster Monitoring** dashboard

## Dashboard Metrics

The pre-configured Kubernetes Cluster Monitoring dashboard includes:

### Performance Metrics
- **Pod CPU Usage (%)**: Real-time CPU usage per pod
- **Pod Memory Usage**: Memory consumption per pod
- **Network I/O**: Network receive/transmit rates per pod

### Health Metrics
- **Pod Restart Count**: Number of restarts per pod (color-coded: green=0, yellow=1-4, red=5+)
- **Container Restarts by Namespace**: Timeline of restarts
- **Pod Status by Namespace**: Pie chart showing Running/Pending/Failed pods

### Cluster Overview
- **Total Pods**: Current number of pods in the cluster
- **Total Services**: Current number of services
- **Total Nodes**: Number of nodes in the cluster
- **Failed Pods**: Count of pods in Failed state (red if > 0)

## Verifying the Installation

Check all monitoring pods are running:
```powershell
kubectl get pods -n monitoring
```

Expected output:
```
NAME                                     READY   STATUS    RESTARTS   AGE
grafana-xxxxx                            1/1     Running   0          Xm
kube-state-metrics-xxxxx                 1/1     Running   0          Xm
prometheus-deployment-xxxxx              1/1     Running   0          Xm
```

Check services:
```powershell
kubectl get svc -n monitoring
```

Expected output:
```
NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
grafana-service      NodePort   x.x.x.x          <none>        3000:30030/TCP   Xm
kube-state-metrics   ClusterIP  x.x.x.x          <none>        8080/TCP         Xm
prometheus-service   NodePort   x.x.x.x          <none>        8080:30090/TCP   Xm
```

## Testing Prometheus Queries

Once Prometheus is accessible, try these sample queries:

1. **Check all targets are up**:
   ```promql
   up
   ```

2. **Pod CPU usage**:
   ```promql
   sum(rate(container_cpu_usage_seconds_total{namespace!="",pod!=""}[5m])) by (pod, namespace)
   ```

3. **Pod memory usage**:
   ```promql
   sum(container_memory_working_set_bytes{namespace!="",pod!=""}) by (pod, namespace)
   ```

4. **Pod restart count**:
   ```promql
   sum(kube_pod_container_status_restarts_total) by (pod, namespace)
   ```

## Customizing the Dashboard

To add more panels to the Grafana dashboard:

1. Open Grafana
2. Navigate to the **Kubernetes Cluster Monitoring** dashboard
3. Click the **Add panel** button
4. Use PromQL queries to fetch metrics from Prometheus
5. Save the dashboard

## Troubleshooting

### Pods not starting
```powershell
kubectl describe pod <pod-name> -n monitoring
kubectl logs <pod-name> -n monitoring
```

### Prometheus not scraping targets
1. Check Prometheus targets: Open Prometheus UI → Status → Targets
2. Verify RBAC permissions are correctly applied
3. Check Prometheus logs:
   ```powershell
   kubectl logs -n monitoring -l app=prometheus-server
   ```

### Grafana dashboard shows "No Data"
1. Verify Prometheus datasource is configured: Grafana → Configuration → Data Sources
2. Check if kube-state-metrics is running:
   ```powershell
   kubectl get pods -n monitoring -l app=kube-state-metrics
   ```
3. Test Prometheus queries directly in Prometheus UI first

## Files in this Directory

- `namespace.yaml`: Monitoring namespace
- `prometheus-rbac.yaml`: Prometheus RBAC resources
- `prometheus-configmap.yaml`: Prometheus configuration
- `prometheus-deployment.yaml`: Prometheus deployment
- `prometheus-service.yaml`: Prometheus service (NodePort)
- `grafana-datasource-config.yaml`: Grafana datasource configuration
- `grafana-dashboard-providers.yaml`: Grafana dashboard providers
- `grafana-dashboards.yaml`: Pre-configured Kubernetes dashboard
- `grafana-deployment.yaml`: Grafana deployment
- `grafana-service.yaml`: Grafana service (NodePort)
- `kube-state-metrics-rbac.yaml`: Kube-state-metrics RBAC
- `kube-state-metrics-deployment.yaml`: Kube-state-metrics deployment
- `kube-state-metrics-service.yaml`: Kube-state-metrics service
- `kubernetes-dashboard.json`: Dashboard JSON (source file)

## Cleanup

To remove all monitoring resources:
```powershell
kubectl delete namespace monitoring
kubectl delete clusterrole prometheus kube-state-metrics
kubectl delete clusterrolebinding prometheus kube-state-metrics
```
