from functools import wraps
from flask import abort
from flask.ext.login import current_user

def permission_required(requiresAdmin):
  def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
      if not current_user.isAdmin() and requiresAdmin:
        abort(403)
      return f(*args, **kwargs)
    return decorated_function
  return decorator

def admin_required(f):
  return permission_required(True)(f)


