import os
import sys
from datetime import date

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, User, StudentProfile, Room, RoomAllocation, Bill, Payment

def seed_sample_data():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed initial hostel rooms if none exist
        if Room.query.count() == 0:
            print("Seeding sample hostel rooms...")
            rooms = [
                Room(room_number="101", room_type="Single Bed", capacity=1, monthly_rent=6000.0, description="Ground floor, attached bathroom, study table, air ventilation."),
                Room(room_number="102", room_type="Double Sharing", capacity=2, monthly_rent=4500.0, description="Ground floor, balcony view, 2 study desks, attached bath."),
                Room(room_number="103", room_type="Double Sharing", capacity=2, monthly_rent=4500.0, description="Ground floor, east facing, dual wardrobes."),
                Room(room_number="201", room_type="Triple Sharing", capacity=3, monthly_rent=3500.0, description="First floor, spacious corner room, 3 lockers."),
                Room(room_number="202", room_type="Single Bed", capacity=1, monthly_rent=6500.0, description="First floor premium single room with AC and balcony."),
                Room(room_number="203", room_type="Dormitory", capacity=4, monthly_rent=2800.0, description="Second floor, 4 single beds, individual study lamps and lockers.")
            ]
            db.session.add_all(rooms)
            db.session.commit()
            print("Sample rooms created.")
        else:
            print("Rooms already exist, skipping room seeding.")

        print("Database seed completed successfully.")

if __name__ == '__main__':
    seed_sample_data()
