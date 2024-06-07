# servidor/__init__.py
from flask import Flask, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

app = Flask(
    __name__, 
    template_folder="/front/templates",
    static_folder="/front/static"
)
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config['DATABASE_URL'] = "sqlite:///katomart.db"
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
app.register_blueprint(api_blueprint)

engine = create_engine(app.config['DATABASE_URL'], connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

Base.metadata.bind = engine

from servidor.models.configs import Configuration
from servidor.models.courses import PlatformAuth
from servidor.models.courses import Platform
from servidor.models.courses import Course
from servidor.models.courses import Module
from servidor.models.courses import Lesson
from servidor.models.courses import File
Base.metadata.create_all(engine)
