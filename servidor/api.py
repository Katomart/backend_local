import os

from flask import jsonify, g, send_from_directory

from .auth import requires_token, requires_consent

from .models.courses import PlatformAuth, Platform, Course, Module, Lesson, File


def setup_main_route(main_bp):
    @main_bp.route('/', defaults={'path': ''})
    @main_bp.route('/<path:path>')
    def catch_all(path):
        static_folder = str(main_bp.static_folder)
        path = str(path) if path else ''
        if path and os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        return send_from_directory(static_folder, 'app.html')


def setup_api_routes(api_blueprint):
    @api_blueprint.route('/ping')
    def ping():
        return jsonify({'message': 'pong'}), 200


    @api_blueprint.route('/get_all_accounts', methods=['GET'])
    @requires_token
    @requires_consent
    def get_all_accounts():
        all_accounts = g.session.query(PlatformAuth).all()
        if all_accounts is None:
            return jsonify({'message': 'No accounts found'}), 404
        return jsonify([account.to_dict() for account in all_accounts]), 200
    
    @requires_token
    @requires_consent
    @api_blueprint.route('/platform_accounts/<int:id>', methods=['GET'])
    def get_account(id):
        auth = g.session.query(PlatformAuth).get(id)
        if auth is None:
            return jsonify({'message': 'Conta não encontrada'}), 404
        return jsonify(auth.to_dict()), 200


    @api_blueprint.route('/get_all_platforms', methods=['GET'])
    @requires_consent
    def get_all_platforms():
        all_platforms = g.session.query(Platform).all()
        if all_platforms is None:
            return jsonify({'message': 'No platforms found'}), 404
        return jsonify([platform.to_dict() for platform in all_platforms]), 200
    
    @api_blueprint.route('/platforms/<int:id>', methods=['GET'])
    @requires_consent
    def get_platform(id):
        platform = g.session.query(Platform).get(id)
        if platform is None:
            return jsonify({'message': 'Plataforma não encontrada'}), 404
        return jsonify(platform.to_dict()), 200
    

    @api_blueprint.route('/get_all_courses')
    @requires_consent
    def get_all_courses():
        all_courses = g.session.query(Course).all()
        if all_courses is None:
            return jsonify({'message': 'Nenhum curso adicionado'}), 404
        return jsonify([course.to_dict() for course in all_courses]), 200

    @api_blueprint.route('/courses/<int:id>', methods=['GET'])
    @requires_consent
    def get_course(id):
        course = g.session.query(Course).get(id)
        if course is None:
            return jsonify({'message': 'Curso não encontrado'}), 404
        return jsonify(course.to_dict()), 200


    @api_blueprint.route('/modules/<int:id>', methods=['GET'])
    @requires_consent
    def get_module(id):
        module = g.session.query(Module).get(id)
        if module is None:
            return jsonify({'message': 'Módulo não encontrado'}), 404
        return jsonify(module.to_dict()), 200


    @api_blueprint.route('/lessons/<int:id>', methods=['GET'])
    @requires_consent
    def get_lesson(id):
        lesson = g.session.query(Lesson).get(id)
        if lesson is None:
            return jsonify({'message': 'Aula não encontrada'}), 404
        return jsonify(lesson.to_dict()), 200


    @api_blueprint.route('/files/<int:id>', methods=['GET'])
    @requires_consent
    def get_file(id):
        file = g.session.query(File).get(id)
        if file is None:
            return jsonify({'message': 'Arquivo não encontrado'}), 404
        return jsonify(file.to_dict()), 200
