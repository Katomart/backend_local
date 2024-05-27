# servidor/__init__.py
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

app = Flask(__name__)
app.config['DATABASE_URL'] = "sqlite:///katomart.db"

engine = create_engine(app.config['DATABASE_URL'], connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

Base.metadata.bind = engine