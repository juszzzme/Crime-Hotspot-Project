from flask import Flask
from config import Config

def create_app(config_class=Config):
    """Application factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from app.extensions import db, login_manager, migrate, csrf
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Import and register auth blueprint if it exists
    try:
        from app.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError:
        pass
    
    # Import and register api blueprint if it exists
    try:
        from app.routes.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
    except ImportError:
        pass
    
    # Import and register visualization blueprint if it exists
    try:
        from app.routes.visualization import bp as visualization_bp
        app.register_blueprint(visualization_bp, url_prefix='/visualization')
    except ImportError as e:
        app.logger.warning(f"Failed to import visualization blueprint: {e}")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
