"""Update password hashes from scrypt to sha256

Revision ID: update_password_hashes
Revises: 977510895f2e
Create Date: 2023-11-30 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = 'update_password_hashes'
down_revision = '977510895f2e'
branch_labels = None
depends_on = None

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = sa.Column(sa.Integer, primary_key=True)
    password_hash = sa.Column(sa.String(255), nullable=False)

def upgrade():
    # Create a connection and session
    bind = op.get_bind()
    session = Session(bind=bind)
    
    try:
        # Get all users
        users = session.query(User).all()
        
        # Update password hashes for all users
        for user in users:
            # Check if the hash is using scrypt
            if user.password_hash.startswith('scrypt:'):
                # Create a temporary password - users will need to reset their passwords
                temp_password = f"temp_{user.id}_password"
                # Generate new hash with sha256
                new_hash = generate_password_hash(temp_password, method='sha256')
                user.password_hash = new_hash
        
        # Commit the changes
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def downgrade():
    # Cannot downgrade as we don't have the original passwords
    pass