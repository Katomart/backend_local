from servidor import create_app
from .config import set_default_config

app = create_app()

if __name__ == '__main__':
    app.run()
