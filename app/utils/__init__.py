import os
import hmac
from hashlib import sha1
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer

from app.config import Config

def generate_confirmation_token(email):
    """Generate a confirmation token for email verification."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    """Confirm the token and return the email if valid."""
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=expiration
        )
    except:
        return False
    return email

__all__ = ['generate_confirmation_token', 'confirm_token']