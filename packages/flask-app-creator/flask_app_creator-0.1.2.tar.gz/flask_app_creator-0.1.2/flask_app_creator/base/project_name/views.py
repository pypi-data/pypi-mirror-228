from flask import Flask


def init_app(app: Flask) -> None:
    @app.get('/')
    def index() -> str:
        return 'Hello World'
