from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'plzchangeit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bollards.db'

db = SQLAlchemy(app)

from bollards_api import routes