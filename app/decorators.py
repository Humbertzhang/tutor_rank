from functools import wraps
from flask import request, jsonify, g
from flask_login import current_user
from .models import User

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_header = request.headers.get('Authorization', None)
        if token_header:
            g.current_user = User.verify_auth_token(token_header)
            if not g.current_user:
                return jsonify({'msg': '403 Forbidden'}), 403
            else:
                return f(*args,**kwargs)
        else:
            return jsonify({'msg': '401 unAuthorization'}), 401
    return wrapper

