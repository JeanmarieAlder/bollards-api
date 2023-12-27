
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="api.env")


class Config:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig():
    SECRET_KEY = os.environ['TEST_FLASK_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False