from flask import jsonify

from .auth import requires_token, requires_consent
from .database import db_session

from .models.courses import PlatformAuth, Platform, Course, Module, Lesson, File

def setup_api_routes(api_blueprint):
    @api_blueprint.route('/ping')
    def ping():
        return jsonify({'message': 'pong'})

    @requires_consent
    @requires_token
    @api_blueprint.route('/get_all_accounts')
    def get_all_accounts():
        all_accounts = PlatformAuth.query.all()
        return jsonify([account.to_dict() for account in all_accounts]), 200
    
