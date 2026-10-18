# BCA Micro-Project Viva Questions & Answers

This document prepares you for examiner questions during your college project presentation and viva examination.

---

### Q1: What is the main objective of your micro-project?
**Answer:** The objective is to develop a secure, functional web application—a **Hostel Management System**—and demonstrate its full containerization using Docker and container orchestration using Kubernetes (Minikube).

---

### Q2: Why did you choose Python Flask over Django or other frameworks?
**Answer:** Flask is a lightweight micro-framework that adheres to the "keep it simple" philosophy suitable for a college micro-project. It allows explicit control over routing, session handling, and database integration without the excessive overhead, boilerplate, or heavyweight background services that Django introduces.

---

### Q3: What is the difference between Docker and a Virtual Machine (VM)?
**Answer:**
- **Virtual Machines** virtualize the underlying hardware. Each VM runs a complete guest operating system (kernel), requiring gigabytes of RAM, minutes to boot, and significant CPU overhead.
- **Docker Containers** virtualize at the operating system level. Containers share the host kernel and run as isolated processes with their own filesystem, libraries, and network namespaces. Containers start in seconds and consume only the memory required by their processes.

---

### Q4: What is the role of Gunicorn in your Docker container? Why not use `flask run`?
**Answer:** Flask's built-in development server is single-threaded, not optimized for concurrency, and explicitly states it is not meant for production. **Gunicorn (Green Unicorn)** is a production-grade WSGI (Web Server Gateway Interface) HTTP server that manages multiple worker processes, handles concurrent requests, handles process restarts, and provides security and stability.

---

### Q5: How do you achieve database persistence in Docker and Kubernetes?
**Answer:**
- **In Docker:** We use a named Docker volume (`hostel_management_db_data`) mounted to `/app/database`. When a container is restarted or replaced with a new image, the SQLite file stored in the volume is preserved.
- **In Kubernetes:** We define a `PersistentVolumeClaim` (`hostel-db-pvc`) which binds a persistent volume on the host. The Pod mounts this PVC to `/app/database`. Even if the Pod crashes or is killed by Kubernetes, the replacement Pod mounts the exact same PVC with all existing student, room, and payment records intact.

---

### Q6: Why did you configure a single replica in your Kubernetes Deployment?
**Answer:** Because our application uses SQLite, which is an embedded, file-based database that relies on operating system file locks. Having multiple independent replicas attempting to write to the same SQLite file simultaneously over a network volume could cause lock contention. In a production enterprise system requiring multi-replica horizontal scale-out, a client-server relational database such as PostgreSQL or MySQL would be deployed.

---

### Q7: What are Kubernetes Liveness and Readiness Probes?
**Answer:**
- **Readiness Probe:** Checks whether the container is ready to accept incoming user traffic. Kubernetes does not route requests to a Pod until its readiness probe succeeds.
- **Liveness Probe:** Periodically checks if the application is healthy. If the web server deadlocks or hangs (failing the probe), Kubernetes automatically terminates and restarts the container to restore service.
- In our project, both probes query the `/health` endpoint every 10–20 seconds.

---

### Q8: How do you handle password security and CSRF protection?
**Answer:**
- Passwords are never stored in plaintext. They are salted and cryptographically hashed using **Werkzeug's PBKDF2/SHA-256** implementation before database persistence.
- Every form uses **Flask-WTF CSRF tokens**. The server validates that incoming POST requests contain a valid, cryptographically signed token matching the client session, preventing Cross-Site Request Forgery attacks.

---

### Q9: How is Role-Based Access Control (RBAC) enforced?
**Answer:** Custom Python decorators (`@admin_required` and `@student_required`) inspect the authenticated user's session before view functions execute. If a student attempts to access an administrator route (such as `/admin/dashboard` or `/admin/fees`), or modify another student's billing data, the server immediately rejects the request with an HTTP 403 Forbidden response.

---

### Q10: How does your fee management system prevent duplicate billing?
**Answer:** At the database level, a composite unique constraint `UniqueConstraint('student_id', 'fee_type', 'billing_period')` is enforced. At the application level, the billing generator verifies whether a bill for that student, fee type, and month already exists before inserting a new record.

---

### Q11: What is the difference between a ConfigMap and a Secret in Kubernetes?
**Answer:**
- **ConfigMap:** Used for storing non-sensitive configuration keys (e.g., `FLASK_ENV`, `DATABASE_DIR`) in plain text.
- **Secret:** Used for sensitive credentials (e.g., `SECRET_KEY`, administrator passwords) that are stored in base64 format and can be restricted with Kubernetes RBAC so developers or cluster observers cannot easily view them.
