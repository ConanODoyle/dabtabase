from flask import Flask
from config import DefaultConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


flaskapp = Flask(__name__)
flaskapp.config.from_object(DefaultConfig)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp, db)
login = LoginManager(flaskapp)
login.login_view = 'login'

if not flaskapp.debug:
	if flaskapp.config['MAIL_SERVER']:
		auth = None
		if flaskapp.config['MAIL_USERNAME'] or flaskapp.config['MAIL_PASSWORD']:
			auth = (flaskapp.config['MAIL_USERNAME'], flaskapp.config['MAIL_PASSWORD'])
		secure = None
		if flaskapp.config['MAIL_USE_TLS']:
			secure = ()
		mail_handler = SMTPHandler(
			mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
		mail_handler.setLevel(logging.ERROR)
		flaskapp.logger.addHandler(mail_handler)

	if not os.path.exists('logs'):
		os.mkdir('logs')
	file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)

	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
	file_handler.setLevel(logging.INFO)
	flaskapp.logger.addHandler(file_handler)

	flaskapp.logger.setLevel(logging.INFO)
	flaskapp.logger.info('Discord logger startup')

from app import routes, models, errors