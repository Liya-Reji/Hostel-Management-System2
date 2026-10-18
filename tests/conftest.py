import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from config import TestingConfig
from models import db, User, StudentProfile, Room, RoomAllocation, Bill, Payment

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    with app.app_context():
        admin = User(username='testadmin', email='admin@test.com', role='admin', is_active=True)
        admin.set_password('AdminPass123!')
        db.session.add(admin)
        db.session.commit()
        return admin.id

@pytest.fixture
def student_user(app):
    with app.app_context():
        user = User(username='teststudent', email='student@test.com', role='student', is_active=True)
        user.set_password('StudentPass123!')
        db.session.add(user)
        db.session.flush()

        profile = StudentProfile(
            user_id=user.id,
            student_id='BCA-TEST-001',
            full_name='Test Student',
            course='BCA 3rd Year',
            phone='9876543210',
            gender='Male'
        )
        db.session.add(profile)
        db.session.commit()
        return user.id, profile.id

@pytest.fixture
def other_student(app):
    with app.app_context():
        user = User(username='otherstudent', email='other@test.com', role='student', is_active=True)
        user.set_password('OtherPass123!')
        db.session.add(user)
        db.session.flush()

        profile = StudentProfile(
            user_id=user.id,
            student_id='BCA-TEST-002',
            full_name='Other Student',
            course='BCA 2nd Year',
            phone='9123456780',
            gender='Female'
        )
        db.session.add(profile)
        db.session.commit()
        return user.id, profile.id
