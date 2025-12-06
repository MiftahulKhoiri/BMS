from flask import abort
from flask_login import current_user

def role_required(min_role):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role < min_role:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator