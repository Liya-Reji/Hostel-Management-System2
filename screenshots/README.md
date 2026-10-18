# Project Screenshots Checklist for BCA Submission

Capture the following screenshots when running your application locally, on Docker, and on Kubernetes to paste into your project report:

---

## 1. Web Application Interfaces
- [ ] **Landing Page (`/`)**: Hero section, key features, and room statistics cards.
- [ ] **Login Screen (`/login`)**: Clean login portal (without credentials or debug notes).
- [ ] **Student Registration (`/register`)**: Student account creation form.
- [ ] **Admin Dashboard (`/admin/dashboard`)**: Metric cards (active students, vacant rooms, pending requests, total billed, collected, outstanding fees).
- [ ] **Student Management (`/admin/students`)**: Student table with search and active status filters.
- [ ] **Room Inventory (`/admin/rooms`)**: Room cards with bed occupancy progress bars and status badges.
- [ ] **Room Request Management (`/admin/requests`)**: Pending room applications with Approve and Reject modals.
- [ ] **Room Allocations (`/admin/allocations`)**: Resident assignments, bed tenancy, transfer, and checkout actions.
- [ ] **Fee Management Dashboard (`/admin/fees`)**: Summary metrics, filtered invoice table, and balance statuses.
- [ ] **Bill Generation Form (`/admin/fees/generate`)**: Single student and bulk billing selection.
- [ ] **Invoice Detail & Payment Form (`/admin/fees/<id>/payment`)**: Recording offline cash/bank/UPI payments and balance breakdown.
- [ ] **Student Dashboard (`/student/dashboard`)**: Student view of allocated room, request status, and dues.
- [ ] **Student Bills & Dues (`/student/bills`)**: Invoices and status badges.
- [ ] **Student Payment Receipts (`/student/payments`)**: List of acknowledged transaction receipts.

---

## 2. Docker & Kubernetes Verification Terminal Outputs
- [ ] **Pytest Results**: Terminal showing `8 passed` in `pytest -v`.
- [ ] **Docker Image Build**: `docker build -t hostel-management-system:latest .`
- [ ] **Docker Containers Running**: `docker ps` showing healthy container status.
- [ ] **Docker Volume Persistence**: Demonstration of container stop/start retaining database records.
- [ ] **Kubernetes Resources**: `kubectl get all,pvc -n hostel-system` showing Pods, Deployments, Services, and PVCs.
- [ ] **Kubernetes Port-Forwarding**: `kubectl port-forward -n hostel-system svc/hostel-service 5000:5000`
- [ ] **Health Check API**: Output of `curl http://localhost:5000/health` returning HTTP 200 JSON status.
