from datetime import datetime, date, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def get_utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'admin' or 'student'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Roll number / College ID
    full_name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)  # e.g. BCA 3rd Year
    phone = db.Column(db.String(20), nullable=False)
    guardian_name = db.Column(db.String(100), nullable=True)
    guardian_phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=False, default='Other')
    address = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    # Relationships
    allocations = db.relationship('RoomAllocation', backref='student', lazy=True, cascade="all, delete-orphan")
    room_requests = db.relationship('RoomRequest', backref='student', lazy=True, cascade="all, delete-orphan")
    bills = db.relationship('Bill', backref='student', lazy=True)

    @property
    def active_allocation(self):
        for alloc in self.allocations:
            if alloc.is_active:
                return alloc
        return None

    @property
    def current_room(self):
        alloc = self.active_allocation
        return alloc.room if alloc else None

    @property
    def total_outstanding(self):
        return sum(b.balance for b in self.bills if b.status != 'Paid')

    def __repr__(self):
        return f'<StudentProfile {self.student_id} - {self.full_name}>'


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    room_type = db.Column(db.String(50), nullable=False, default='Single')  # Single, Double, Triple, Dormitory
    capacity = db.Column(db.Integer, nullable=False, default=1)
    monthly_rent = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    # Relationships
    allocations = db.relationship('RoomAllocation', backref='room', lazy=True)
    requests = db.relationship('RoomRequest', backref='room', lazy=True)

    @property
    def current_occupancy(self):
        return sum(1 for a in self.allocations if a.is_active)

    @property
    def is_full(self):
        return self.current_occupancy >= self.capacity

    @property
    def available_beds(self):
        return max(0, self.capacity - self.current_occupancy)

    @property
    def status(self):
        occ = self.current_occupancy
        if occ == 0:
            return 'Vacant'
        elif occ < self.capacity:
            return 'Partially Occupied'
        else:
            return 'Full'

    def __repr__(self):
        return f'<Room {self.room_number} ({self.status})>'


class RoomRequest(db.Model):
    __tablename__ = 'room_requests'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='SET NULL'), nullable=True)
    request_date = db.Column(db.DateTime, default=get_utc_now, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)  # 'Pending', 'Approved', 'Rejected'
    remarks = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<RoomRequest #{self.id} Student {self.student_id} Status {self.status}>'


class RoomAllocation(db.Model):
    __tablename__ = 'room_allocations'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id', ondelete='RESTRICT'), nullable=False)
    allocated_date = db.Column(db.Date, default=date.today, nullable=False)
    checkout_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    monthly_rent = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<RoomAllocation Student {self.student_id} Room {self.room_id} Active {self.is_active}>'


class Bill(db.Model):
    __tablename__ = 'bills'
    __table_args__ = (
        db.UniqueConstraint('student_id', 'fee_type', 'billing_period', name='uq_student_fee_period'),
    )

    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id', ondelete='RESTRICT'), nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # 'Hostel Rent', 'Mess Fee', 'Electricity', 'Other'
    billing_period = db.Column(db.String(30), nullable=False)  # e.g., 'October 2026'
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='Pending', nullable=False)  # 'Pending', 'Partially Paid', 'Paid', 'Overdue'
    created_at = db.Column(db.DateTime, default=get_utc_now)

    # Payments associated with this bill
    payments = db.relationship('Payment', backref='bill', lazy=True, cascade="all, delete-orphan")

    @property
    def total_paid(self):
        return round(sum(p.amount for p in self.payments), 2)

    @property
    def balance(self):
        rem = round(self.amount - self.total_paid, 2)
        return max(0.0, rem)

    def recalculate_status(self):
        """Update and return the status based on paid amount, balance, and due date."""
        bal = self.balance
        today = date.today()
        if bal <= 0.0:
            self.status = 'Paid'
        elif self.total_paid > 0.0:
            if today > self.due_date:
                self.status = 'Overdue'
            else:
                self.status = 'Partially Paid'
        else:
            if today > self.due_date:
                self.status = 'Overdue'
            else:
                self.status = 'Pending'
        return self.status

    def __repr__(self):
        return f'<Bill {self.bill_number} - {self.fee_type} - {self.status}>'


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, default=date.today, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False, default='Cash')  # Cash, Bank Transfer, Cheque, UPI Receipt
    reference_note = db.Column(db.String(255), nullable=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    def __repr__(self):
        return f'<Payment {self.receipt_number} - Amount {self.amount}>'
