from functools import wraps
from flask import g, request, redirect, url_for
from werkzeug.exceptions import Forbidden

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if hasattr(g, 'user') and g.user.primary_group.admin:
            return func(*args, **kwargs)
        raise Forbidden("You do not have access")
    return decorated_function
