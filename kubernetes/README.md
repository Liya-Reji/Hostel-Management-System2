# Kubernetes Deployment Guide (Minikube & kubectl on Windows)

This guide provides step-by-step instructions for deploying the **Hostel Management System** onto a local Kubernetes cluster using **Minikube** and **kubectl** on Windows PowerShell.

---

## 1. Prerequisites Installation (Windows)

### A. Install kubectl
If not already installed, install `kubectl` via PowerShell using winget or Chocolatey:
```powershell
winget install -e --id Kubernetes.kubectl
# Verify installation
kubectl version --client
```

### B. Install Minikube
Install Minikube on Windows:
```powershell
winget install -e --id Kubernetes.minikube
# Verify installation
minikube version
```

---

## 2. Start Minikube Cluster

Start Minikube using the Docker driver:
```powershell
minikube start --driver=docker --cpus=2 --memory=2048
```
Verify the cluster status:
```powershell
minikube status
kubectl get nodes
```

---

## 3. Build & Load the Docker Image

To allow Minikube to access your local Docker image without needing to push to Docker Hub:

### Option A: Configure Shell to Use Minikube's In-Cluster Docker Daemon (Recommended)
Run the following in Windows PowerShell:
```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t hostel-management-system:latest .
```
*(This builds the image directly inside Minikube's Docker daemon, making it instantly available to Pods).*

### Option B: Build Locally and Load Image into Minikube
```powershell
docker build -t hostel-management-system:latest .
minikube image load hostel-management-system:latest
```

### Option C: Push to Docker Hub (If desired)
```powershell
docker tag hostel-management-system:latest <your-dockerhub-username>/hostel-management-system:latest
docker push <your-dockerhub-username>/hostel-management-system:latest
# Then update image field in kubernetes/deployment.yaml to match your repository name
```

---

## 4. Deploy Manifests to Kubernetes

Navigate to the project root in PowerShell:

```powershell
# 1. Create the dedicated namespace
kubectl apply -f kubernetes/namespace.yaml

# 2. Apply ConfigMap for application environment variables
kubectl apply -f kubernetes/configmap.yaml

# 3. Create Secret from template (or apply custom secret)
# Copy example if secret.yaml does not exist:
if (-not (Test-Path "kubernetes/secret.yaml")) {
    Copy-Item "kubernetes/secret.yaml.example" "kubernetes/secret.yaml"
}
kubectl apply -f kubernetes/secret.yaml

# 4. Apply PersistentVolumeClaim for SQLite database persistence
kubectl apply -f kubernetes/pvc.yaml

# 5. Apply Deployment (includes health probes, resource limits, and volume mounts)
kubectl apply -f kubernetes/deployment.yaml

# 6. Apply Service to expose the web interface
kubectl apply -f kubernetes/service.yaml
```

---

## 5. Verify & Inspect Resources

Check status across all deployed resources:
```powershell
# View Pods, Deployments, Services, and PVCs in the namespace
kubectl get all,pvc -n hostel-system -o wide
```

Expected output:
- Pod status: `Running` (1/1 Ready)
- Service `hostel-service`: `NodePort` on port `5000:30050/TCP`
- PVC `hostel-db-pvc`: `Bound`

Inspect Pod logs:
```powershell
kubectl logs -n hostel-system -l app=hostel-web -f
```

---

## 6. Access the Application

### Option A: Using kubectl Port-Forwarding (Simplest & Most Reliable)
```powershell
kubectl port-forward -n hostel-system svc/hostel-service 5000:5000
```
Open your browser and navigate to: `http://localhost:5000`

### Option B: Using Minikube Service URL
```powershell
minikube service hostel-service -n hostel-system --url
```

---

## 7. Initialize Admin Account in Kubernetes Pod

Execute a secure one-off shell in the running Pod to initialize the administrator account:
```powershell
# Get the pod name
$POD_NAME = (kubectl get pods -n hostel-system -l app=hostel-web -o jsonpath='{.items[0].metadata.name}')

# Run admin creation script inside the container
kubectl exec -it -n hostel-system $POD_NAME -- python scripts/create_admin.py --username admin --email admin@hostel.edu --password AdminPass123!
```

---

## 8. Verifying Data Persistence

1. Log into the application at `http://localhost:5000` as admin.
2. Register a student or add a new room (e.g. Room 301).
3. Restart or delete the Pod to simulate a node or pod crash:
   ```powershell
   kubectl delete pod -n hostel-system -l app=hostel-web
   ```
4. Wait for Kubernetes to automatically recreate the Pod (`kubectl get pods -n hostel-system`).
5. Refresh the website in your browser: all rooms, students, and billing records remain intact because the SQLite file is mounted to the persistent volume `hostel-db-pvc`.

---

## 9. Demonstrating Scaling, Rolling Updates, and Rollback

### Scaling Note (SQLite Architectural Limitation)
Because SQLite operates via direct local file locks, running multiple concurrent replicas against the same SQLite file on a network share can lead to lock contention. For high-availability multi-replica scale-out, a client-server database like PostgreSQL or MySQL is used in production.

To demonstrate scaling up and down during your viva:
```powershell
# Scale to 2 replicas (demonstration)
kubectl scale deployment hostel-deployment -n hostel-system --replicas=2
kubectl get pods -n hostel-system

# Scale back to 1 replica for persistent SQLite stability
kubectl scale deployment hostel-deployment -n hostel-system --replicas=1
```

### Rolling Update & Rollback Demonstration
```powershell
# View rollout history
kubectl rollout history deployment/hostel-deployment -n hostel-system

# Simulate updating image version
kubectl set image deployment/hostel-deployment hostel-web-app=hostel-management-system:latest -n hostel-system

# Check rollout status
kubectl rollout status deployment/hostel-deployment -n hostel-system

# Rollback if needed
kubectl rollout undo deployment/hostel-deployment -n hostel-system
```

---

## 10. Cleaning Up Kubernetes Resources

When finished with your demonstration:
```powershell
kubectl delete namespace hostel-system
```
