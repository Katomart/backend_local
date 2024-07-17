import shutil
import os

from flask import jsonify, g, send_from_directory

from .auth import requires_token, requires_consent

from .models.courses import PlatformAuth, Platform, Course, Module, Lesson, File
from .models.configs import Configuration

from .install import try_auto_install_tp_tool

def setup_main_route(main_bp):
    @main_bp.route('/', defaults={'path': ''})
    @main_bp.route('/<path:path>')
    def catch_all(path):
        if path != "" and os.path.exists(main_bp.static_folder + '/' + path):
            return send_from_directory(main_bp.static_folder, path)
        else:
            return send_from_directory(main_bp.static_folder, 'index.html')


def setup_api_routes(api_blueprint):
    TP_IDS = {
        1: 'ffmpeg',
        2: 'geckodriver',
        3: 'bento4'
    }

    @api_blueprint.route('/ping', methods=['GET'])
    def ping():
        return jsonify({'message': 'pong'}), 200
    
    @api_blueprint.route('/test_route', methods=['GET'])
    def test_route():
        return jsonify(), 200
    
    @api_blueprint.route('/get_katomart_password', methods=['GET'])
    def get_katomart_password():  # Método a ser implementado no futuro.
        password = g.session.query(Configuration).filter_by(key='user_local_password').first()
        if password is None:
            return jsonify({'status': False, 'message': 'No password found'}), 404
        return jsonify({'status': True, 'message': password.to_dict()}), 200

    @api_blueprint.route('/get_katomart_consent', methods=['GET'])
    def get_katomart_consent():
        consent = g.session.query(Configuration).filter_by(key='setup_user_local_consent_date').first()
        if consent is None:
            return jsonify({'status': False, 'message': 'No consent found'}), 404
        return jsonify({'status': True, 'message': consent.to_dict()}), 200
    
    @api_blueprint.route('/get_all_configurations', methods=['GET'])
    def get_all_configurations():
        all_configurations = g.session.query(Configuration).all()
        if not all_configurations:
            return jsonify({'status': False, 'message': 'No configurations found'}), 404
        return jsonify({'status': True, 'message': [configuration.to_dict() for configuration in all_configurations]}), 200
    
    @api_blueprint.route('/configurations/<int:id>', methods=['GET'])
    @requires_consent
    def get_configuration(id):
        configuration = g.session.query(Configuration).get(id)
        if configuration is None:
            return jsonify({'status': False, 'message': 'Configuration not found'}), 404
        return jsonify({'status': True, 'message': configuration.to_dict()}), 200

    @api_blueprint.route('/configurations/<int:id>', methods=['UPDATE'])
    @requires_consent
    def update_configuration(id):
        configuration = g.session.query(Configuration).get(id)
        if configuration is None:
            return jsonify({'status': False, 'message': 'Configuration not found'}), 404
        configuration.update(g.request.json)
        return jsonify({'status': True, 'message': configuration.to_dict()}), 200
    
    @api_blueprint.route('/check_third_party_tool/<int:id>', methods=['GET'])
    @requires_consent
    def check_third_party_tool(id):
        #tp reads like toilet paper lmao
        has_tool = shutil.which(TP_IDS.get(id))
        if has_tool is None:
            tool = g.session.query(Configuration).filter_by(key=f'install_{TP_IDS.get(id)}').first()
            if not tool['value']:
                return jsonify({'status': False, 'message': f'{TP_IDS.get(id)} not present and not marked for installation!'}), 404
            else:
                return jsonify({'status': False, 'message': f'{TP_IDS.get(id)} not present but marked for installation! Proceeding with install...'}), 404
        return jsonify({'status': True, 'message': f'{TP_IDS.get(id)} is present and should be working fine.'}), 200
    
    @api_blueprint.route('/auto_install_third_party_tool/<int:id>', methods=['GET'])
    @requires_consent
    def auto_install_third_party_tool(id):
        user_os = g.session.query(Configuration).filter_by(key='user_os').first()
        if user_os['value'] not in ('linux', 'darwin', 'win32'):
            return jsonify({'status': False, 'message': 'Unsupported OS'}), 404
        
        if id not in TP_IDS.keys():
            return jsonify({'status': False, 'message': 'Invalid tool ID'}), 404
        
        r = try_auto_install_tp_tool(TP_IDS.get(id))
        if not r:
            return jsonify({'status': False, 'message': f'{TP_IDS.get(id)} failed to install!'}), 404
        return jsonify({'status': True, 'message': f'{TP_IDS.get(id)} installed successfully!'}), 200
    
    @api_blueprint.route('/install_third_party_tool', methods=['GET'])
    @requires_consent
    def install_third_party_tool():
        return jsonify({'status': False, 'message': 'This route is not implemented yet!'}), 404


    @api_blueprint.route('/get_all_accounts', methods=['GET'])
    @requires_consent
    def get_all_accounts():
        all_accounts = g.session.query(PlatformAuth).all()
        if all_accounts is None:
            return jsonify({'message': 'No accounts found'}), 404
        return jsonify([account.to_dict() for account in all_accounts]), 200
    
    @api_blueprint.route('/platform_accounts/<int:id>', methods=['GET'])
    @requires_consent
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
