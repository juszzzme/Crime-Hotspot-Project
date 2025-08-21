from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()

# Import User model here to avoid circular imports
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate()
