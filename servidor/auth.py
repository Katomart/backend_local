from functools import wraps
from flask import request, jsonify

def token_is_valid(token):
    # Placeholder
    return token == "katomart"

def protected_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Missing Authorization.'}), 403

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({'message': 'Invalid Token.'}), 403

        if not token_is_valid(token):
            return jsonify({'message': 'Invalid or expired Token.'}), 403

        return f(*args, **kwargs)
    return decorated_function
