
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from bollards_api.config import Config
from dotenv import load_dotenv


# take environment variables from api.env
load_dotenv(dotenv_path='api.env')

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bollards_api.api.routes import api
    from bollards_api.bollards.routes import bollards
    from bollards_api.errors.handlers import errors
    from bollards_api.main.routes import main
    from bollards_api.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(bollards)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app
