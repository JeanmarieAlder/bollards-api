# Based on the example from flask
# https://github.com/pallets/flask/blob/2.0.2/examples/tutorial/tests/conftest.py

import pytest
from bollards_api import create_app, db
from bollards_api.config import TestConfig
from bollards_api import db
from tests.utils.db import add_default_user, reset_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(config_class=TestConfig)
    with app.app_context():
        reset_db()
        add_default_user()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="noob", password="password"):
        return self._client.post(
            "/login", 
            data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)