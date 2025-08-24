#!/usr/bin/env python3
"""
Database initialization script for Crime Hotspot Project
Creates tables and adds demo users for testing
"""

from app import create_app
from app.extensions import db
from app.models.user import User

def init_database():
    """Initialize database with demo users."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if demo user already exists
        existing_user = User.query.filter_by(email='admin@crimesense.com').first()
        if existing_user:
            print("Demo user already exists!")
            return
        
        # Create demo users
        print("Creating demo users...")
        
        # Admin user
        admin_user = User(
            email='admin@crimesense.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            password='admin123',  # This will be hashed automatically
            is_active=True,
            is_admin=True,
            email_confirmed=True
        )
        
        # Regular user
        demo_user = User(
            email='user@crimesense.com',
            username='user',
            first_name='Demo',
            last_name='User',
            password='user123',  # This will be hashed automatically
            is_active=True,
            is_admin=False,
            email_confirmed=True
        )
        
        # Test user
        test_user = User(
            email='demo@crimesense.com',
            username='demo',
            first_name='Test',
            last_name='User',
            password='demo123',  # This will be hashed automatically
            is_active=True,
            is_admin=False,
            email_confirmed=True
        )
        
        # Add users to database
        db.session.add(admin_user)
        db.session.add(demo_user)
        db.session.add(test_user)
        
        try:
            db.session.commit()
            print("✅ Database initialized successfully!")
            print("\n📋 Demo Credentials:")
            print("Admin: admin@crimesense.com / admin123")
            print("User:  user@crimesense.com / user123")
            print("Demo:  demo@crimesense.com / demo123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating users: {e}")

if __name__ == '__main__':
    init_database()
