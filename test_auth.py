#!/usr/bin/env python3
"""
Test authentication system and debug login issues
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from werkzeug.security import check_password_hash, generate_password_hash

def test_password_hashing():
    """Test password hashing and verification"""
    print("🔐 Testing password hashing...")
    
    test_password = "admin123"
    
    # Test different hashing methods
    methods = ['pbkdf2:sha256', 'pbkdf2:sha1', 'scrypt', 'argon2']
    
    for method in methods:
        try:
            hashed = generate_password_hash(test_password, method=method)
            verified = check_password_hash(hashed, test_password)
            print(f"✅ {method}: Hash created and verified successfully")
        except Exception as e:
            print(f"❌ {method}: Error - {e}")

def test_database_users():
    """Test database users without circular imports"""
    print("\n📊 Testing database users...")
    
    try:
        # Import Flask app components carefully
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config import Config
        
        # Create minimal app
        app = Flask(__name__)
        app.config.from_object(Config)
        db = SQLAlchemy(app)
        
        # Define User model inline to avoid circular imports
        from datetime import datetime
        from flask_login import UserMixin
        from werkzeug.security import generate_password_hash, check_password_hash
        
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
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            
            def verify_password(self, password):
                return check_password_hash(self.password_hash, password)
        
        with app.app_context():
            # Query users
            users = User.query.all()
            print(f"Found {len(users)} users in database:")
            
            for user in users:
                print(f"  📧 Email: {user.email}")
                print(f"  👤 Username: {user.username}")
                print(f"  ✅ Active: {user.is_active}")
                print(f"  🔑 Admin: {user.is_admin}")
                print(f"  🔐 Password Hash: {user.password_hash[:50]}...")
                
                # Test password verification
                test_passwords = ['admin123', 'user123', 'demo123']
                for pwd in test_passwords:
                    if user.verify_password(pwd):
                        print(f"  ✅ Password '{pwd}' works for {user.email}")
                        break
                else:
                    print(f"  ❌ None of the test passwords work for {user.email}")
                print()
                
    except Exception as e:
        print(f"❌ Database test failed: {e}")

def test_manual_verification():
    """Manually test password verification"""
    print("\n🧪 Manual password verification test...")
    
    # Test with known hash
    test_password = "admin123"
    test_hash = generate_password_hash(test_password, method='pbkdf2:sha256')
    
    print(f"Original password: {test_password}")
    print(f"Generated hash: {test_hash}")
    print(f"Verification result: {check_password_hash(test_hash, test_password)}")
    print(f"Wrong password test: {check_password_hash(test_hash, 'wrongpassword')}")

if __name__ == '__main__':
    print("🔍 Authentication System Debug Tool")
    print("=" * 50)
    
    test_password_hashing()
    test_manual_verification()
    test_database_users()
