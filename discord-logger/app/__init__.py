from flask import Flask
from config import DefaultConfig

flaskapp = Flask(__name__)
flaskapp.config.from_object(DefaultConfig)

from app import routes