from functools import wraps
from flask import request, jsonify
from .database import get_session
from .models.configs import Configuration

def token_is_valid(token):
    # Placeholder
    return token == "katomart"

def requires_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or ' ' not in auth_header:
            return jsonify({'message': 'Missing Authorization.'}), 403

        token_type, token = auth_header.split(' ', 1)
        if token_type.lower() != 'bearer':
            return jsonify({'message': 'Invalid Token Type.'}), 403

        if not token_is_valid(token):
            return jsonify({'message': 'Invalid or Expired Token.'}), 403

        return f(*args, **kwargs)
    return decorated_function

def requires_consent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Decorated function")
        db_session = get_session()  # get_session() deve retornar uma sessão pronta para usar

        consent = db_session.query(Configuration).filter_by(key='user_local_consent').first()
        db_session.close()  # Garante que a sessão seja fechada após a consulta

        if consent and consent.value.lower() == 'true':
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'DENIED. You must consent to the ToS to use this application.'}), 403

    return decorated_function
