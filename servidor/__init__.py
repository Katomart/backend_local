from flask import Flask
from .database import init_db, db_session
from .blueprints import register_blueprints

from .config import DevelopmentConfig, TestingConfig, ProductionConfig

from .config import set_default_config

def create_app(config_name='default'):
    app = Flask(__name__, template_folder="/front/templates", static_folder="/front/static")

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    app.config.from_object(configs[config_name])

    register_blueprints(app)
    with app.app_context():
        init_db(app)
        set_default_config()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db_session is not None:
            db_session.remove()

    return app

