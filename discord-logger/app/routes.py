from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import flaskapp, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@flaskapp.route("/")
@flaskapp.route("/index")
@login_required
def index():
	user = {"username": "Miguel"}
	posts = [
		{
			"author": {"username": "John"},
			"body": "My Post"
		},
		{
			"author": user,
			"body": "e"
		}
	]
	return render_template("index.html", **{"title": "test", "posts": posts})


@flaskapp.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	loginform = LoginForm()
	if loginform.validate_on_submit():
		user = User.query.filter_by(username=loginform.username.data).first()
		if user is None or not user.check_password(loginform.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=loginform.remember_me.data)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')

		return redirect(next_page)

	return render_template("login.html", title="Sign In", form=loginform)


@flaskapp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@flaskapp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	registerform = RegistrationForm()
	if registerform.validate_on_submit():
		user = User(username=registerform.username.data, email=registerform.email.data)
		user.set_password(registerform.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Registration successful!')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form=registerform)