from flask import Blueprint
from .api import setup_api_routes

def register_blueprints(app):
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    setup_api_routes(api_blueprint)
    app.register_blueprint(api_blueprint)
