from app import flaskapp, db
from app.models import User, Post

@flaskapp.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}