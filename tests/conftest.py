from pytest import fixture
from flask.testing import FlaskClient, FlaskCliRunner
from app.infraestructure.database.config import TestingConfig
from app.server import create_app

@fixture(scope='module')
def app():
    app = create_app(config_class=TestingConfig)
    # other setup can go here
    yield app
    # clean up / reset resources here
    
@fixture()
def client(app) -> FlaskClient:
    return app.test_client()

@fixture()
def request_context(app) -> FlaskClient:
    return app.test_request_context()

@fixture()
def runner(app) -> FlaskCliRunner:
    return app.test_cli_runner()