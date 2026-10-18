# Docker Practical Guide & Command Reference

This practical guide explains the containerization of the **Hostel Management System** and provides complete Windows PowerShell commands for your college project demonstration.

---

## 1. Core Docker Concepts Explained

| Concept | Explanation in this Project |
| :--- | :--- |
| **Docker Image** | A lightweight, standalone, executable package containing everything needed to run the application (Python runtime, dependencies, application code, Gunicorn). Defined by `Dockerfile`. |
| **Docker Container** | A runnable instance of a Docker image. The container runs isolated from other processes on the host machine. |
| **Port Mapping (`-p 5000:5000`)** | Forwards host port `5000` to container port `5000`. Requests to `http://localhost:5000` on your Windows machine reach Gunicorn inside the container. |
| **Environment Variables (`-e`)** | Configuration injected at runtime (e.g. `FLASK_ENV=production`, `SECRET_KEY=...`) keeping credentials out of image layers. |
| **Volumes (`-v`)** | Persistent storage independent of the container lifecycle. Mounted to `/app/database`, ensuring SQLite files survive container removal. |
| **Container Networking** | Allows containers to communicate with each other and host networks via bridge or custom networks created by Docker Compose. |

---

## 2. Dockerfile Breakdown

```dockerfile
# 1. Base Image: Slim Debian-based Python image
FROM python:3.11-slim

# 2. Performance & Logs settings
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# 3. Working Directory inside the container
WORKDIR /app

# 4. Install system tools needed for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# 5. Dependency Caching: Copy requirements first
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application code
COPY . /app/

# 7. Persistent directory for SQLite database
RUN mkdir -p /app/database

# 8. Expose web port
EXPOSE 5000

# 9. Docker Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 10. Startup: Initialize schema and start Gunicorn WSGI server
CMD ["sh", "-c", "python scripts/init_db.py && python scripts/seed_sample_data.py && gunicorn --bind 0.0.0.0:5000 --workers 2 app:app"]
```

---

## 3. Step-by-Step PowerShell Commands

Open Windows PowerShell in `D:\Hostel-Management`:

### A. Build the Docker Image
```powershell
docker build -t hostel-management-system:latest .
```
Verify the created image:
```powershell
docker images | Select-String "hostel-management-system"
```

### B. Create a Persistent Docker Volume
```powershell
docker volume create hostel_db_data
```

### C. Run the Container
```powershell
docker run -d `
  --name hostel_web_app `
  -p 5000:5000 `
  -e SECRET_KEY="my-production-secret-key" `
  -v hostel_db_data:/app/database `
  --restart unless-stopped `
  hostel-management-system:latest
```

### D. Verify Container Status & Health Check
```powershell
docker ps
```
Look for `(healthy)` in the `STATUS` column after ~15 seconds.

Test the health endpoint directly:
```powershell
curl http://localhost:5000/health
```
Expected output:
```json
{"database":"connected","environment":"production","status":"healthy"}
```

### E. Inspect Application Logs
```powershell
# View recent logs
docker logs hostel_web_app

# Follow live output
docker logs -f hostel_web_app
```

### F. Create the Administrator Account Inside Container
```powershell
docker exec -it hostel_web_app python scripts/create_admin.py --username admin --email admin@hostel.edu --password AdminPass123!
```

### G. Test Database Persistence
1. Access `http://localhost:5000` and log in with the administrator account.
2. Add a new room (e.g., Room 401) or register a student.
3. Stop and remove the container:
   ```powershell
   docker stop hostel_web_app
   docker rm hostel_web_app
   ```
4. Re-run a brand new container using the same persistent volume:
   ```powershell
   docker run -d `
     --name hostel_web_app `
     -p 5000:5000 `
     -e SECRET_KEY="my-production-secret-key" `
     -v hostel_db_data:/app/database `
     hostel-management-system:latest
   ```
5. Refresh your browser at `http://localhost:5000`: Room 401 and all registered records are still present!

---

## 4. Docker Compose Workflow (Recommended)

Docker Compose simplifies multi-step deployment into single commands:

### A. Start the Application
```powershell
docker compose up -d --build
```

### B. View Running Services
```powershell
docker compose ps
```

### C. View Real-Time Logs
```powershell
docker compose logs -f
```

### D. Restart Application
```powershell
docker compose restart
```

### E. Stop and Clean Up
```powershell
# Stop containers (preserves database volume)
docker compose down

# Stop containers AND delete volume (use only for complete reset)
docker compose down -v
```

---

## 5. Tagging and Publishing to Docker Hub

If you wish to demonstrate publishing to Docker Hub under your personal account:

```powershell
# 1. Log in to Docker Hub
docker login

# 2. Tag your local image with your Docker Hub username
docker tag hostel-management-system:latest <your-dockerhub-username>/hostel-management-system:v1.0

# 3. Push image to Docker Hub
docker push <your-dockerhub-username>/hostel-management-system:v1.0
```
This image can now be pulled on any server or Kubernetes cluster worldwide.
