from flask import render_template, redirect, url_for, request, flash, session

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired

from .. import app, db
from .. import models
from .. import forms
from .. import util

from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager() #Initilize flask-login
login_manager.init_app(app)
login_manager.login_view = "login_user_page"

class UsernamePasswordForm(forms.SQLForm):
	"""Login form for local users. Bypassed completley (that is, all empty/false) for OAuth"""
	username = StringField("Username")
	local_login=BooleanField("Local Login")
	password = PasswordField("Password")

class UserDataForm(UsernamePasswordForm):
	name = StringField("Name")
	email = StringField("Email")
	marss_id = IntegerField("MARSS ID")

@login_manager.user_loader
def load_user(session_token):
	"""Helper function for flask-login"""
	return models.User.query.filter_by(session_token=session_token).first()

@app.route('/register', methods=['GET', 'POST'])
def register_user_page():
	if request.method=='GET':
		return render_template("register.html", form=UserDataForm())

	form=UserDataForm(request.form)
	if form.validate(): #If valid...
		user=models.User.empty() #Create empty user
		form.fill_to(user) #Fil it from the form
		user.role='view' #Set it to view
		user.enabled=False #And disabled, so that admins must enable the acct.
		user.set_password(form.password.data) #Set the password
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
			f.username.data=request.args["user"] #If we have a QS term for user (from just registering) fill it in
		return render_template("login.html", form=f)

	form=UsernamePasswordForm(request.form)
	if form.validate():
		if form.local_login.data: #If using local auth
			user=models.User.query.filter_by(username=form.username.data).first()
			if not user or not user.check_password(form.password.data): #if invalid login...
				flash("Invalid Username/Password", 'error')
				return render_template("login.html", form=form)
			return util.try_login_user(user, url_for("home")) #Proceed to final login step
		else:
			return redirect(url_for("oauth_login")) #If they didnt tick the box, send them on to OAuth login
	else:
		util.flash_form_errors(form)
		return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout_user_page():
    logout_user()
    session.pop('google_token', None) #Pop the google token
    flash("Logged out")
    return redirect(url_for('login_user_page'))