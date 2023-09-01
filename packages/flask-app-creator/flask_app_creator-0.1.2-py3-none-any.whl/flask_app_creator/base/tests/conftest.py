import pytest
from flask import Flask
from flask.testing import FlaskClient
from project_name.app import create_app


@pytest.fixture(scope='module')
def app() -> Flask:
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture(scope='module')
def client(app: Flask) -> FlaskClient:
    return app.test_client()
