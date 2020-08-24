from flask import Flask
from config import DefaultConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

flaskapp = Flask(__name__)
flaskapp.config.from_object(DefaultConfig)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp, db)
login = LoginManager(flaskapp)
login.login_view = 'login'

from app import routes, models