from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

db_session = scoped_session(sessionmaker())

def init_db(app):
    global db_session
    engine = create_engine(app.config['DATABASE_URL'], echo=True, connect_args={"check_same_thread": False})
    db_session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
