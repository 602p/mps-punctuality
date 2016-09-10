import contextlib
from flask import flash, redirect, url_for
from flask_login import current_user, login_user
from . import models
import functools

@contextlib.contextmanager
def ignored(*exceptions):
	"""Handy dandy context manager"""
	try:
		yield
	except exceptions:
		pass

def flash_form_errors(form):
	"""Show all errors in a WTForm nicely"""
	[flash("Invalid data in item '%s': %s" % (k,", ".join(v)), 'error')
		for k,v in form.errors.items()]

def require_user_role(role):
	"""Decorator for route functions that requires the users role to be greater-than-or-equal-to role"""
	def _wrap(func):
		@functools.wraps(func)
		def _wrapped(*a, **k):
			if models.ROLE_HIERARCHY.index(role)<=models.ROLE_HIERARCHY.index(current_user.role): #TODO: Use Enums
				return func(*a,**k)
			else:
				flash("You do not have the permission to access this", 'error')
				return redirect(url_for('home'))
		return _wrapped
	return _wrap

def try_login_user(user, redir="/"):
	"""Final user login stage. Block users that are incomplete (no role) or are not enabled"""
	if user.enabled and user.role:
		flash("Success! Logged in as %s" % user.username)
		login_user(user) #Actual login step here
		return redirect(redir)
	else:
		flash("Please wait for an Administrator to enable your account", 'error')
		return redirect(url_for("login_user_page"))