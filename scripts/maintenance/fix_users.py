#!/usr/bin/env python3
"""
Fix user authentication by recreating users with correct password hashes
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def fix_users():
    """Fix users in database with correct password hashing"""
    print("🔧 Fixing user authentication...")
    
    # Create minimal app
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    
    # Define User model inline
    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(255), unique=True, nullable=False)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        first_name = db.Column(db.String(50))
        last_name = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
        is_admin = db.Column(db.Boolean, default=False)
        email_confirmed = db.Column(db.Boolean, default=False)
        email_confirmed_on = db.Column(db.DateTime, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        
        def set_password(self, password):
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        def verify_password(self, password):
            return check_password_hash(self.password_hash, password)
    
    with app.app_context():
        # Clear all existing users
        print("🗑️ Clearing existing users...")
        User.query.delete()
        db.session.commit()
        
        # Create demo users with correct password hashing
        print("👥 Creating demo users...")
        
        # Admin user
        admin_user = User(
            email='admin@crimesense.com',
            username='admin',
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_admin=True,
            email_confirmed=True
        )
        admin_user.set_password('admin123')
        
        # Regular user
        demo_user = User(
            email='user@crimesense.com',
            username='user',
            first_name='Demo',
            last_name='User',
            is_active=True,
            is_admin=False,
            email_confirmed=True
        )
        demo_user.set_password('user123')
        
        # Test user
        test_user = User(
            email='demo@crimesense.com',
            username='demo',
            first_name='Test',
            last_name='User',
            is_active=True,
            is_admin=False,
            email_confirmed=True
        )
        test_user.set_password('demo123')
        
        # Add users to database
        db.session.add(admin_user)
        db.session.add(demo_user)
        db.session.add(test_user)
        
        try:
            db.session.commit()
            print("✅ Demo users created successfully!")
            
            # Verify users
            print("\n🔍 Verifying users...")
            users = User.query.all()
            for user in users:
                print(f"📧 {user.email} - Testing password...")
                test_passwords = {
                    'admin@crimesense.com': 'admin123',
                    'user@crimesense.com': 'user123',
                    'demo@crimesense.com': 'demo123'
                }
                
                expected_password = test_passwords.get(user.email)
                if expected_password and user.verify_password(expected_password):
                    print(f"  ✅ Password verification successful")
                else:
                    print(f"  ❌ Password verification failed")
            
            print("\n📋 Demo Credentials:")
            print("Admin: admin@crimesense.com / admin123")
            print("User:  user@crimesense.com / user123")
            print("Demo:  demo@crimesense.com / demo123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating users: {e}")

if __name__ == '__main__':
    fix_users()
