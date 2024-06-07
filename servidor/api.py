from flask import jsonify

def setup_api_routes(api_blueprint):
    @api_blueprint.route('/ping')
    def ping():
        return jsonify({'message': 'pong'})

    @api_blueprint.route('/user_content', methods=['GET'])
    def user_content():
        return jsonify({'message': 'user content'})
