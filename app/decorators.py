from functools import wraps
from flask import request, jsonify
from flask_login import current_user
from .models import User

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_header = request.headers.get('Authorization', None)
        if token_header:
            decode_token = base64.b64decode(token_header)
            g.current_user = User.verify_auth_token(decode_token)
            if not User.query.filter_by(id=g.current_user):
                return jsonify({'message': '403 Forbidden'}), 403
            else:
                return f(*args,**kwargs)
        else:
            return jsonify({'message': '401 unAuthorization'}), 401
    return decorated

