import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db

def init_db():
    app = create_app()
    with app.app_context():
        print("Initializing database tables...")
        db.create_all()
        print("Database schema verified and initialized successfully.")

if __name__ == '__main__':
    init_db()
