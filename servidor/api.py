import os

from flask import jsonify, g, send_from_directory

from .auth import requires_token, requires_consent

from .models.courses import PlatformAuth, Platform, Course, Module, Lesson, File
from .models.configs import Configuration

from .install import try_auto_install_bento4


def setup_main_route(main_bp):
    @main_bp.route('/', defaults={'path': ''})
    @main_bp.route('/<path:path>')
    def catch_all(path):
        if path != "" and os.path.exists(main_bp.static_folder + '/' + path):
            return send_from_directory(main_bp.static_folder, path)
        else:
            return send_from_directory(main_bp.static_folder, 'index.html')


def setup_api_routes(api_blueprint):
    @api_blueprint.route('/ping', methods=['GET'])
    def ping():
        return jsonify({'message': 'pong'}), 200
    
    @api_blueprint.route('/test_route', methods=['GET'])
    def test_route():
        return jsonify(try_auto_install_bento4()), 200
    
    @api_blueprint.route('/get_katomart_password', methods=['GET'])
    def get_katomart_password():
        password = g.session.query(Configuration).filter_by(key='user_local_password').first()
        if password is None:
            return jsonify({'status': False, 'message': 'No password found'}), 403
        return jsonify({'status': True, 'message': password.to_dict()}), 200
    
    @api_blueprint.route('/get_katomart_consent', methods=['GET'])
    def get_katomart_consent():
        has_consented = g.session.query(Configuration).filter_by(key='user_local_consent').first()
        consent_date = g.session.query(Configuration).filter_by(key='user_local_consent_date').first()
        if has_consented is None:
            return jsonify({'status': False, 'message': 'No consent found'}), 403
        return jsonify({
            'status': True,
            'message': consent_date.to_dict() if consent_date else 'No consent date found'
        }), 200
    
    @api_blueprint.route('/get_all_configurations', methods=['GET'])
    def get_all_configurations():
        all_configurations = g.session.query(Configuration).all()
        if not all_configurations:
            return jsonify({'status': False, 'message': 'No configurations found'}), 404
        return jsonify([configuration.to_dict() for configuration in all_configurations]), 200


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
