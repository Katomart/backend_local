from flask import jsonify, g

from .auth import requires_token, requires_consent

from .models.courses import PlatformAuth, Platform, Course, Module, Lesson, File

def setup_api_routes(api_blueprint):
    @api_blueprint.route('/ping')
    def ping():
        return jsonify({'message': 'pong'}), 200


    @api_blueprint.route('/get_all_accounts')
    @requires_token
    @requires_consent
    def get_all_accounts():
        all_accounts = g.session.query(PlatformAuth).all()
        return jsonify([account.to_dict() for account in all_accounts]), 200
    
    @api_blueprint.route('/get_all_platforms')
    @requires_consent
    def get_all_platforms():
        all_platforms = g.session.query(Platform).all()
        return jsonify([platform.to_dict() for platform in all_platforms]), 200
    
    @api_blueprint.route('/get_all_courses')
    @requires_consent
    def get_all_courses():
        all_courses = g.session.query(Course).all()
        return jsonify([course.to_dict() for course in all_courses]), 200
