# Kubernetes Practical Guide & Orchestration Reference

This guide covers container orchestration for the **Hostel Management System** using Kubernetes (`kubectl` and `minikube`).

---

## 1. Kubernetes Architecture & Concepts

| Resource | Role in this Project |
| :--- | :--- |
| **Namespace (`hostel-system`)** | Logical boundary isolating the hostel application resources from other workloads. |
| **Pod** | Smallest deployable compute unit in Kubernetes. Runs our containerized Flask + Gunicorn web app. |
| **Deployment (`hostel-deployment`)** | Manages Pod replication, declarative desired state, health checks, self-healing, rolling updates, and rollbacks. |
| **ConfigMap (`hostel-config`)** | Stores non-confidential configuration (e.g. `FLASK_ENV=production`, `DATABASE_DIR=/app/database`). |
| **Secret (`hostel-secret`)** | Stores sensitive base64-encoded strings (`SECRET_KEY`, `ADMIN_PASSWORD`) separate from Pod definitions. |
| **PersistentVolumeClaim (`hostel-db-pvc`)** | Requests persistent storage from the cluster (1Gi) to preserve `hostel.db` SQLite database across Pod restarts. |
| **Service (`hostel-service`)** | Provides a stable network endpoint (NodePort on port 5000:30050) targeting the application Pods. |
| **Liveness & Readiness Probes** | Periodic healthchecks against `/health`. Liveness restarts dead containers; Readiness stops sending traffic until the Pod is fully ready. |

---

## 2. Complete PowerShell Deployment Commands

### A. Cluster Startup
```powershell
# Start Minikube with Docker driver
minikube start --driver=docker

# Verify cluster connectivity
kubectl cluster-info
kubectl get nodes
```

### B. Make Docker Image Available to Minikube
```powershell
# Set Minikube Docker environment in Windows PowerShell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Build image inside Minikube's Docker daemon
docker build -t hostel-management-system:latest .
```

### C. Deploy Manifests in Sequence
```powershell
# 1. Namespace
kubectl apply -f kubernetes/namespace.yaml

# 2. ConfigMap
kubectl apply -f kubernetes/configmap.yaml

# 3. Secret
if (-not (Test-Path "kubernetes/secret.yaml")) {
    Copy-Item "kubernetes/secret.yaml.example" "kubernetes/secret.yaml"
}
kubectl apply -f kubernetes/secret.yaml

# 4. PersistentVolumeClaim
kubectl apply -f kubernetes/pvc.yaml

# 5. Deployment
kubectl apply -f kubernetes/deployment.yaml

# 6. Service
kubectl apply -f kubernetes/service.yaml
```

---

## 3. Inspection and Monitoring Commands

### View All Resources
```powershell
kubectl get all,pvc -n hostel-system
```

### Detailed Pod Inspection
```powershell
# Describe Pod to view events, probe results, and mount status
$POD_NAME = (kubectl get pods -n hostel-system -l app=hostel-web -o jsonpath='{.items[0].metadata.name}')
kubectl describe pod $POD_NAME -n hostel-system
```

### Stream Live Logs
```powershell
kubectl logs -f $POD_NAME -n hostel-system
```

---

## 4. Access the Application

### Method 1: Port-Forwarding (Recommended for Windows)
```powershell
kubectl port-forward -n hostel-system svc/hostel-service 5000:5000
```
Open your browser at `http://localhost:5000`.

### Method 2: Minikube Service URL
```powershell
minikube service hostel-service -n hostel-system
```

---

## 5. Live Demonstration Scenarios for Viva

### Scenario 1: Self-Healing Pod Recovery
Simulate a container crash by deleting the active Pod:
```powershell
kubectl delete pod -n hostel-system -l app=hostel-web
# Watch Kubernetes immediately provision a replacement Pod
kubectl get pods -n hostel-system -w
```

### Scenario 2: Data Persistence Verification
Because the SQLite database is mounted to `hostel-db-pvc`, when Kubernetes recreates the Pod, all rooms, allocations, and billing history remain completely intact.

### Scenario 3: Rolling Update & Zero-Downtime Rollout
```powershell
# View revision history
kubectl rollout history deployment/hostel-deployment -n hostel-system

# Trigger an update
kubectl set env deployment/hostel-deployment -n hostel-system UPDATE_TRIGGER="v1.1"

# Monitor status
kubectl rollout status deployment/hostel-deployment -n hostel-system

# Rollback to previous revision
kubectl rollout undo deployment/hostel-deployment -n hostel-system
```

---

## 6. Common Deployment Failures and Troubleshooting

| Failure Symptom | Cause | Diagnostic Command & Fix |
| :--- | :--- | :--- |
| `ErrImageNeverPull` / `ImagePullBackOff` | The image does not exist inside Minikube's Docker daemon. | Run `minikube image load hostel-management-system:latest` or configure `& minikube -p minikube docker-env --shell powershell \| Invoke-Expression` before building. |
| `CrashLoopBackOff` | Application crashed on startup (missing secret or DB error). | Run `kubectl logs -n hostel-system <pod-name>` to view Python traceback. |
| `Pending` PVC | StorageClass provisioner issue or insufficient disk space. | Run `kubectl describe pvc hostel-db-pvc -n hostel-system`. |
| Probes Failing | Application took longer than `initialDelaySeconds` to start. | Adjust `initialDelaySeconds` in `kubernetes/deployment.yaml`. |
