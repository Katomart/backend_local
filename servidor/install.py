import pathlib

from .database import get_session
from .models.configs import Configuration


def try_auto_install_ffmpeg():
    pass

def try_auto_install_geckodriver():
    pass

def try_auto_install_bento4():
    db_session = get_session()
    try:
        should_install = db_session.query(Configuration).filter_by(key='install_bento4').first()
        return should_install.to_dict()
    except Exception as e:
        print('Error trying to auto install Bento4:', e)
        db_session.rollback()