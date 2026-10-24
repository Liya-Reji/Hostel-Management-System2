# Hostel Management System (HostelHub)

**Course:** Bachelor of Computer Applications (BCA)  
**Project Category:** Web Application Development, Containerization & Orchestration Micro-Project  
**Technologies:** Python Flask, Bootstrap 5, SQLite, Gunicorn, Docker, Docker Compose, Kubernetes (Minikube / kubectl), pytest  

---

## 1. Abstract

The **Hostel Management System** is a secure, lightweight, and containerized web application developed to streamline hostel administration in colleges and universities. Traditional manual hostel tracking often leads to administrative bottlenecks, room over-allocation, delayed fee collections, and scattered paper receipts. 

This project solves these challenges by providing role-based portals for administrators and student residents. Administrators can track bed capacity in real-time, approve or reject room applications, allocate residents without exceeding room limits, generate recurring monthly bills (rent, mess, utilities), and acknowledge offline payments with automatic balance reconciliation. Students can register accounts, view available rooms, submit room requests, track their allocation status, monitor fee dues, and access payment receipts.

Beyond its core business logic, the application is packaged as an enterprise-ready micro-project demonstrating modern DevOps workflows: containerization with **Docker**, multi-container orchestration with **Docker Compose**, and deployment with self-healing, rolling updates, and persistent volume storage on **Kubernetes**.

---

## 2. Problem Statement

College micro-project requirement:
> *"Develop a web application of your choice and deploy it using Docker containers and Kubernetes. Demonstrate containerization, deployment, and management of the application."*

Hostel administration presents a prime operational scenario:
1. **Inefficient Room Allocation:** Manual room registers lead to duplicate assignments, booking past capacity, and lack of real-time vacancy tracking.
2. **Scattered Billing & Dues Tracking:** Monthly rent, mess, and electricity fees frequently incur errors, duplicate invoices, and lost paper payment receipts.
3. **Deployment Volatility:** Modern web applications must not depend on fragile local machine configurations. They must be packaged with their dependencies, run reliably across any infrastructure, survive host restarts without data loss, and scale gracefully.

---

## 3. Objectives & Scope

### Objectives
1. Implement a complete, secure, responsive web portal for hostel wardens and student residents.
2. Enforce strict database integrity: zero room over-allocations, zero duplicate room numbers, and prevention of duplicate monthly bills.
3. Deliver a robust offline fee management module calculating partial payments and overdue statuses accurately.
4. Containerize the application using **Docker** and **Gunicorn** with native health checking and persistent volume storage.
5. Deploy and orchestrate the workload on **Kubernetes** using Namespaces, ConfigMaps, Secrets, PVCs, Deployments, and Services.
6. Verify 100% of functional requirements using automated **pytest** unit and integration tests.

### Scope
- **Included:** Administrator operations, student registration, room inventory, allocation transfers, checkout, multi-category fee billing, offline payment recording, session security, Docker containerization, and Kubernetes manifests.
- **Excluded (by design):** Online payment gateway integration (mocked via official offline receipt acknowledgments) and multi-region cloud clustering.

---

## 4. Main Features

### A. Administrator Module
- **Dashboard Overview:** Live summary cards showing active students, total rooms, occupied rooms, vacant rooms, pending requests, total billed, total fees collected, and overdue invoices.
- **Student Resident Management:** Register new students, search by roll number or name, filter active/deactivated records, view room tenancy history, and safely deactivate accounts.
- **Room Inventory & Capacity Tracking:** Add/edit rooms with specific capacities (Single, Double, Triple, Dormitory), real-time bed vacancy progress bars, and deletion protection for occupied rooms.
- **Room Request Workflow:** Review student accommodation applications with one-click **Approve** and **Reject** modals including custom administrative remarks.
- **Room Allocation Engine:** Assign approved students to rooms. Enforces capacity bounds and ensures no student holds multiple active room allocations. Supports room transfers and checkout.
- **Comprehensive Fee Management:**
  - Generate single or bulk bills for all active hostel residents for a selected period.
  - Multi-category fees: *Hostel Rent*, *Mess Fee*, *Electricity & Utilities*, *Maintenance*, *Other Charges*.
  - Strict prevention of duplicate monthly invoices for the same student and category.
  - Record offline payments (Cash, Bank Transfer, NEFT, UPI receipt) supporting partial payments.
  - Automated status calculation: `Pending`, `Partially Paid`, `Paid`, `Overdue`.
  - Edit or cancel bills safely if no payment receipts have been recorded.

### B. Student Resident Module
- **Self-Service Registration & Login:** Clean, secure signup with college roll number and password hashing.
- **Personal Dashboard:** Real-time visibility into current room assignment, application status, and fee balance.
- **Browse Available Rooms:** Inspect room photos/descriptions, facilities, and open bed counts.
- **Room Application Submission:** Submit accommodation preferences with special requests.
- **My Room & Roommates:** View details of assigned room, tenancy start date, and current roommates.
- **Invoices & Dues:** View all issued bills, due dates, breakdown of amounts paid, and remaining balance.
- **Payment Receipts History:** Official transaction log with unique receipt numbers for college audit records.
- **Profile & Password Management:** Update contact/guardian details and securely change login credentials.

---

## 5. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons | Responsive UI with navy blue (`#0f2b48`), teal (`#0d9488`), and white theme. |
| **Backend** | Python 3.11+ / Flask 3.0 | Web application routing, WSGI dispatch, and business logic. |
| **Database** | SQLite 3 via Flask-SQLAlchemy (SQLAlchemy 2.0 ORM) | Relational database with parameterized queries and persistent volume storage. |
| **Form Security** | Flask-WTF & WTForms | Server-side validation and CSRF protection. |
| **WSGI Server** | Gunicorn 21.2 | Multi-worker HTTP application server for Docker container runtime. |
| **Testing** | pytest 8.2 | Automated functional, authorization, security, and integration testing. |
| **Containerization** | Docker & Docker Compose | Container packaging, multi-stage layer caching, and named persistent volumes. |
| **Orchestration** | Kubernetes (`kubectl` & Minikube) | Self-healing Pods, Deployments, Services, ConfigMaps, Secrets, and PVCs. |

---

## 6. System Architecture & Database Design

### Database Schema (ER Summary)
- `users`: Core authentication table (`id`, `username`, `email`, `password_hash`, `role`, `is_active`, `created_at`).
- `student_profiles`: Resident information linked 1:1 with `users` (`student_id`, `full_name`, `course`, `phone`, `gender`, `guardian_name`, `address`).
- `rooms`: Room inventory (`room_number`, `room_type`, `capacity`, `monthly_rent`, `is_available`).
- `room_requests`: Student applications (`student_id`, `room_id`, `status`, `remarks`, `reviewed_at`).
- `room_allocations`: Active tenancy and history (`student_id`, `room_id`, `monthly_rent`, `allocated_date`, `checkout_date`, `is_active`).
- `bills`: Monthly invoices (`bill_number`, `student_id`, `fee_type`, `billing_period`, `amount`, `due_date`, `status`). Enforces `UniqueConstraint('student_id', 'fee_type', 'billing_period')`.
- `payments`: Official offline transaction receipts (`receipt_number`, `bill_id`, `amount`, `payment_date`, `payment_mode`, `reference_note`).

*For full architectural and sequence diagrams, refer to [docs/architecture.md](docs/architecture.md).*

---

## 7. Project Folder Structure

```text
Hostel-Management-System/
├── app.py                      # Main Flask application with routes, RBAC decorators & handlers
├── config.py                   # Environment-aware configuration (Development, Production, Testing)
├── models.py                   # SQLAlchemy ORM models and business rules
├── forms.py                    # Flask-WTF input validation forms with CSRF protection
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── Dockerfile                  # Production container definition with Gunicorn & healthcheck
├── docker-compose.yml          # Multi-container Compose manifest with persistent volume
├── .dockerignore               # Build context exclusions
├── .env.example                # Environment variables template
├── .gitignore                  # Git exclusions for secrets, databases, and caches
├── README.md                   # Main project documentation
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout with navbar, alerts & footer
│   ├── index.html              # Landing page
│   ├── login.html              # Clean authentication page (no exposed credentials)
│   ├── register.html           # Student self-registration
│   ├── errors/                 # Custom 400, 403, 404, 500 error pages
│   ├── admin/                  # Wardens / Administrator management templates
│   │   ├── dashboard.html      # Metrics & quick actions
│   │   ├── students.html       # Student list & search
│   │   ├── student_form.html   # Add / Edit student
│   │   ├── student_view.html   # Student detail & billing history
│   │   ├── rooms.html          # Room inventory & bed progress bars
│   │   ├── room_form.html      # Add / Edit room
│   │   ├── requests.html       # Review room applications (Approve / Reject)
│   │   ├── allocations.html    # Room tenancy, transfer, checkout
│   │   ├── allocation_form.html# Allocate student to room
│   │   ├── change_room.html    # Transfer room
│   │   ├── fees.html           # Fee dashboard, metrics & invoice table
│   │   ├── bill_form.html      # Single & bulk bill generation
│   │   ├── bill_view.html      # Invoice details & payment log
│   │   ├── bill_edit.html      # Edit invoice
│   │   └── payment_form.html   # Record offline payment
│   └── student/                # Student resident self-service templates
│       ├── dashboard.html      # Resident dashboard
│       ├── profile.html        # Profile management
│       ├── change_password.html# Secure password change
│       ├── rooms.html          # Browse available rooms
│       ├── request_room.html   # Submit accommodation request
│       ├── allocation.html     # My room & roommates
│       ├── bills.html          # Invoices & fee dues
│       ├── bill_view.html      # Invoice view
│       └── payments.html       # Official payment receipts
├── static/
│   ├── css/custom.css          # Navy/teal styling, cards, status badges
│   └── js/main.js              # Auto-dismiss alerts & UI utilities
├── database/                   # Persistent SQLite directory (mounted to volume)
├── scripts/                    # Management CLI utilities
│   ├── init_db.py              # Safe schema initialization
│   ├── create_admin.py         # Protected administrator account creation CLI
│   └── seed_sample_data.py     # Sample room seeding utility
├── tests/                      # Automated test suite
│   ├── conftest.py             # Test fixtures & isolated memory database
│   └── test_all_features.py    # 8 comprehensive integration test cases
├── kubernetes/                 # Kubernetes orchestration manifests
│   ├── namespace.yaml          # Dedicated namespace
│   ├── configmap.yaml          # Non-sensitive configuration
│   ├── secret.yaml.example     # Secret template
│   ├── pvc.yaml                # Persistent volume claim for database
│   ├── deployment.yaml         # Pod deployment with health probes
│   ├── service.yaml            # NodePort service exposing port 5000
│   └── README.md               # Kubernetes execution guide
├── docs/                       # Project documentation
│   ├── architecture.md         # Application & deployment architecture
│   ├── docker-guide.md         # Docker practical with PowerShell commands
│   ├── kubernetes-guide.md     # Kubernetes practical with PowerShell commands
│   └── viva-questions.md       # College viva questions and answers
└── screenshots/
    └── README.md               # Checklist for report screenshots
```

---

## 8. Windows Installation & Local Setup

### Step 1: Clone Repository & Create Virtual Environment
Open Windows PowerShell:
```powershell
# Navigate to workspace
cd D:\Hostel-Management

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Initialize Database Schema
```powershell
python scripts/init_db.py
python scripts/seed_sample_data.py
```

### Step 4: Create Initial Administrator Account Securely
```powershell
python scripts/create_admin.py --username admin --email admin@hostel.edu --password AdminPass123!
```

### Step 5: Start Local Development Server
```powershell
python app.py
```
Access the application at `http://localhost:5000`.

---

## 9. Automated Testing (pytest)

Run the automated test suite verifying all 8 major functional areas:
```powershell
.\venv\Scripts\pytest -v
```
All tests execute in an isolated in-memory database without modifying real records:
```text
tests/test_all_features.py::test_homepage_and_health_endpoint PASSED     [ 12%]
tests/test_all_features.py::test_user_registration_and_login PASSED      [ 25%]
tests/test_all_features.py::test_rbac_authorization PASSED               [ 37%]
tests/test_all_features.py::test_room_management_and_duplicate_prevention PASSED [ 50%]
tests/test_all_features.py::test_room_request_and_allocation_rules PASSED [ 62%]
tests/test_all_features.py::test_billing_duplicate_prevention_payments_and_balance PASSED [ 75%]
tests/test_all_features.py::test_overdue_fee_handling PASSED             [ 87%]
tests/test_all_features.py::test_student_privacy_and_access_restrictions PASSED [100%]
======================= 8 passed in 1.77s =======================
```

---

## 10. Docker Build & Deployment

### Build the Image
```powershell
docker build -t hostel-management-system:latest .
```

### Run Container with Persistent Volume & Health Check
```powershell
docker run -d `
  --name hostel_web_app `
  -p 5000:5000 `
  -e SECRET_KEY="production-secret-key-change-me" `
  -v hostel_management_db_data:/app/database `
  --restart unless-stopped `
  hostel-management-system:latest
```

### Verify Container Health
```powershell
docker ps
curl http://localhost:5000/health
```

### Using Docker Compose
```powershell
# Start container in background
docker compose up -d --build

# Inspect logs
docker compose logs -f

# Stop container
docker compose down
```

*For comprehensive Docker instructions, refer to [docs/docker-guide.md](docs/docker-guide.md).*

---

## 11. Kubernetes Deployment (Minikube & kubectl)

Deploy the workload to a local Kubernetes cluster:

```powershell
# 1. Start Minikube
minikube start --driver=docker

# 2. Build or load image into Minikube
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
docker build -t hostel-management-system:latest .

# 3. Apply Kubernetes Manifests
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
if (-not (Test-Path "kubernetes/secret.yaml")) { Copy-Item "kubernetes/secret.yaml.example" "kubernetes/secret.yaml" }
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/pvc.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

# 4. Port Forward to Access in Browser
kubectl port-forward -n hostel-system svc/hostel-service 5000:5000
```
Open `http://localhost:5000` in your web browser.

*For detailed orchestration commands, scaling, rolling update, and rollback demonstrations, refer to [docs/kubernetes-guide.md](docs/kubernetes-guide.md).*

---

## 12. Troubleshooting

| Issue | Resolution |
| :--- | :--- |
| **Port 5000 already in use** | Find and terminate the process using `netstat -ano \| findstr :5000` or map to another port (e.g., `-p 5050:5000`). |
| **CSRF Token Missing / Expired** | Ensure cookies are enabled in your browser and submit forms directly from the rendered web pages. |
| **Database changes not persisting in Docker** | Ensure `-v hostel_management_db_data:/app/database` is specified so that the SQLite file is written to the mounted volume rather than the container's ephemeral root. |

---

## 13. Limitations & Future Enhancements

### Current Architectural Limitations
1. **Single-Replica SQLite Concurrency:** SQLite is file-based; while ideal for a micro-project demonstration, a multi-pod horizontal scale-out in high-traffic enterprise production requires a networked database such as PostgreSQL or MySQL.
2. **Offline Payment Acknowledgments:** Payments are currently recorded by administrative staff upon receiving cash, cheque, or UPI slips.

### Future Enhancements
1. Integration with a payment gateway (e.g., Razorpay or Stripe) for instant online rent clearance.
2. Biometric and RFID gate pass integration for student hostel curfew logging.
3. Automated email and SMS alerts for upcoming fee due dates.

---

## 14. Conclusion

The **Hostel Management System** successfully satisfies all requirements of the BCA college micro-project. It showcases a complete end-to-end engineering lifecycle: structured database modeling, secure authentication, intuitive responsive UI design, automated test verification, production container packaging with Docker, and resilient deployment with self-healing and data persistence on Kubernetes.
