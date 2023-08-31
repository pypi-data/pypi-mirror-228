from importlib import import_module

import toml
from flask import Flask


def init_app(app: Flask) -> None:
    config = toml.load(open('config.toml', 'r'))
    secret_config = toml.load(open('.secret.toml', 'r'))
    for extension in config['extensions']:
        module = import_module(extension)
        module.init_app(app)
    app.config['SECRET_KEY'] = secret_config['secret_key']
