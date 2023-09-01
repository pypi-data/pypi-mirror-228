from flask import Flask

from . import config


def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', template_folder='templates')
    config.init_app(app)
    return app
