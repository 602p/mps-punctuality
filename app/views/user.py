from flask import render_template, redirect, url_for, request, flash

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

from .. import app, db
from .. import models
from .. import forms

from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(app)

class UsernamePasswordForm(forms.SQLForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])

class UserDataForm(UsernamePasswordForm):
	name = StringField("Name")
	email = StringField("Email")
	marss_id = IntegerField("MARSS ID")
	role = StringField("Role")			#TODO: REMOVE ME IN PRODUCTION
	enabled = BooleanField("Enabled")	#TODO: REMOVE ME IN PRODUCTION

@login_manager.user_loader
def load_user(session_token):
	return models.User.query.filter_by(session_token=session_token).one()

@app.route('/register', methods=['GET', 'POST'])
def register_user_page():
	if request.method=='GET':
		return render_template("register.html", form=UserDataForm())

	form=UserDataForm(request.form)
	if form.validate():
		user=models.User.empty()
		form.fill_to(user)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login_user_page')+"?user="+form.username.data)
	else:
		return render_template("register.html", form=form, error=str(form.errors))

@app.route("/login", methods=['GET', 'POST'])
def login_user_page():
	if request.method=='GET':
		return render_template("login.html", form=UsernamePasswordForm(), username=request.args.get("user"))

	form=UsernamePasswordForm(request.form)
	if form.validate():
		user=models.User.query.filter_by(username=form.username.data).first()
		if not user or not user.check_password(form.password.data):
			return render_template("login.html", form=form, error="Invalid Username or Password")
		login_user(user)
		flash("Success! Logged in as %s" % user.username)
		return redirect(url_for("home"))
	else:
		return render_template("login.html", form=form, error=str(form.errors))