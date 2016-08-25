from flask import render_template, redirect, url_for, request, flash

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

from .. import app, db
from .. import models
from .. import forms
from .. import util

from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_user_page"

class UsernamePasswordForm(forms.SQLForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class UserDataForm(UsernamePasswordForm):
	name = StringField("Name")
	email = StringField("Email")
	marss_id = IntegerField("MARSS ID")

@login_manager.user_loader
def load_user(session_token):
	return models.User.query.filter_by(session_token=session_token).first()

@app.route('/register', methods=['GET', 'POST'])
def register_user_page():
	if request.method=='GET':
		return render_template("register.html", form=UserDataForm())

	form=UserDataForm(request.form)
	if form.validate():
		user=models.User.empty()
		form.fill_to(user)
		user.role='view'
		user.enabled=False
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login_user_page')+"?user="+form.username.data)
	else:
		util.flash_form_errors(form)
		return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_user_page():
	if request.method=='GET':
		f=UsernamePasswordForm()
		if "user" in request.args:
			f.username.data=request.args["user"]
		return render_template("login.html", form=f)

	form=UsernamePasswordForm(request.form)
	if form.validate():
		user=models.User.query.filter_by(username=form.username.data).first()
		if not user.enabled:
			flash("Please wait for an administrator to enable your account", 'error')
			return render_template("login.html", form=form)
		if not user or not user.check_password(form.password.data):
			flash("Invalid username or password", 'error')
			return render_template("login.html", form=form)
		login_user(user)
		flash("Success! Logged in as %s" % user.username)
		return redirect(url_for("home"))
	else:
		util.flash_form_errors(form)
		return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout_user_page():
    logout_user()
    flash("Logged out")
    return redirect(url_for('login_user_page'))