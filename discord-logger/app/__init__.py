from flask import Flask
from config import DefaultConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flaskapp = Flask(__name__)
flaskapp.config.from_object(DefaultConfig)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp, db)

from app import routes, models