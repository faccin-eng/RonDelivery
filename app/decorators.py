from functools import wraps
from flask import session, redirect, url_for, abort

def empresa_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("empresa_id"):
            return redirect(url_for("empresa.login_empresa"))
        return f(*args, **kwargs)
    return decorated_function