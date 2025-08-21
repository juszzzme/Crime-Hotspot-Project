from flask_login import current_user, login_required
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return decorated_function
