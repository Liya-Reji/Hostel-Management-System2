import os
import sys
import argparse
import getpass

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, User

def create_admin(username=None, email=None, password=None):
    app = create_app()
    with app.app_context():
        db.create_all()

        username = username or os.environ.get('ADMIN_USERNAME')
        email = email or os.environ.get('ADMIN_EMAIL')
        password = password or os.environ.get('ADMIN_PASSWORD')

        if not username:
            username = input("Enter Admin Username: ").strip()
        if not email:
            email = input("Enter Admin Email: ").strip()
        if not password:
            password = getpass.getpass("Enter Admin Password: ").strip()
            confirm = getpass.getpass("Confirm Admin Password: ").strip()
            if password != confirm:
                print("Error: Passwords do not match.")
                sys.exit(1)

        if not username or not email or not password:
            print("Error: Username, email, and password cannot be empty.")
            sys.exit(1)

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            if existing.is_admin:
                print(f"Admin user '{existing.username}' already exists. Updating password...")
                existing.set_password(password)
                existing.email = email
                existing.is_active = True
                db.session.commit()
                print(f"Admin password for '{existing.username}' updated successfully.")
                return
            else:
                print(f"Error: A user with username/email already exists as '{existing.role}'.")
                sys.exit(1)

        admin = User(
            username=username,
            email=email,
            role='admin',
            is_active=True
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Administrator account '{username}' created successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create or update an administrator account.")
    parser.add_argument('--username', help="Admin username")
    parser.add_argument('--email', help="Admin email")
    parser.add_argument('--password', help="Admin password")
    args = parser.parse_args()

    create_admin(args.username, args.email, args.password)
