from flask import flash, redirect, url_for
from flask_login import login_user
from . import models

def try_login_user(user, redir="/"):
	if user.enabled and user.role:
		flash("Success! Logged in as %s" % user.username)
		login_user(user)
		return redirect(redir)
	else:
		flash("Please wait for an Administrator to enable your account", 'error')
		return redirect(url_for("login_user_page"))