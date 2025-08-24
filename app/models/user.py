from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from app.extensions import db
from app.utils import generate_confirmation_token, confirm_token


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships are set up in relationships.py to avoid circular imports
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email:
            self.email = self.email.lower()
        if hasattr(self, 'name') and not (hasattr(self, 'first_name') and hasattr(self, 'last_name')):
            # Handle case where name is provided as a single field
            name_parts = self.name.split(' ', 1)
            self.first_name = name_parts[0]
            self.last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        # Use pbkdf2:sha256 method which is widely supported
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def generate_auth_token(self, expiration=3600):
        """Generate an authentication token for API access."""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id}, salt='auth-token')

    @staticmethod
    def verify_auth_token(token):
        """Verify the authentication token."""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='auth-token', max_age=3600)
            return User.query.get(data['id'])
        except:
            return None

    def generate_email_confirmation_token(self, expiration=3600):
        """Generate a confirmation token for email verification."""
        return generate_confirmation_token(self.email)

    @staticmethod
    def confirm_email_token(token, expiration=3600):
        """Confirm the email token and return the user if valid."""
        email = confirm_token(token, expiration)
        if not email:
            return None
        return User.query.filter_by(email=email).first()

    def has_role(self, role_name):
        """Check if user has a specific role"""
        # For now, we only have is_admin flag
        if role_name == 'admin':
            return self.is_admin
        return False
    
    def can(self, permission):
        """Check if user has a specific permission"""
        # Basic permission system - can be expanded
        if self.is_admin:
            return True
        return False
    
    def __repr__(self):
        return f'<User {self.email}>'
