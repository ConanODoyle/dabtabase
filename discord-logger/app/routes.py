from flask import render_template, flash, redirect, url_for
from app import flaskapp
from app.forms import LoginForm


@flaskapp.route("/")
@flaskapp.route("/index")
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
	return render_template("index.html", **{"user": user, "title": "test", "posts": posts})


@flaskapp.route("/login", methods=["GET", "POST"])
def login():
	loginform = LoginForm()
	if loginform.validate_on_submit():
		flash("Login requested for user {}, remember_me={}".format(loginform.username.data, loginform.remember_me.data))
		return redirect(url_for('index'))

	return render_template("login.html", title="Sign In", form=loginform)