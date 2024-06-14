from functools import wraps
from flask import request, jsonify

from sqlalchemy.orm import Session
from .database import db_session
from .models.configs import Configuration

def token_is_valid(token):
    # Placeholder
    return token == "katomart"

def requires_token(f):
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

def requires_consent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session = Session(bind=db_session.get_bind())
        
        consent = session.query(Configuration).filter_by(key='user_local_consent').first()
        session.close()

        if consent and consent.enabled and consent.value.lower() == 'true':
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'DENIED. You must consent to the ToS to use this application.'}), 403

    return decorated_function
