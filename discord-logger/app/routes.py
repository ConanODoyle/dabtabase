from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import flaskapp, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm


@flaskapp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


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


@flaskapp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1 <script>alert(\'hi\');</script>'},
		{'author': user, 'body': 'Test post #2'},
	]
	followform = EmptyForm()
	return render_template('user.html', user=user, posts=posts, form=followform)


@flaskapp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	editprofileform = EditProfileForm(current_user.username)
	if editprofileform.validate_on_submit():
		checkuser = User.query.filter_by(username=editprofileform.username.data).first()
		current_user.username = editprofileform.username.data
		current_user.about_me = editprofileform.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		editprofileform.username.data = current_user.username
		editprofileform.about_me.data = current_user.about_me

	return render_template('edit_profile.html', title='Edit Profile', form=editprofileform)


@flaskapp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for('user', username=username))
		current_user.follow(user)
		db.session.commit()
		flash('You are following {}!'.format(username))
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))


@flaskapp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for('user', username=username))
		current_user.unfollow(user)
		db.session.commit()
		flash('You are not following {}.'.format(username))
		return redirect(url_for('user', username=username))
	else:
		return redirect(url_for('index'))