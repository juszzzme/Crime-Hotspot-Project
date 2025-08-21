# Import all route blueprints here
from .main import bp as main_bp
from .auth import bp as auth_bp
from .api import bp as api_bp
from .visualization import bp as visualization_bp

__all__ = ['main_bp', 'auth_bp', 'api_bp', 'visualization_bp']
