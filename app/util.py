import contextlib
from flask import flash, redirect, url_for
from flask_login import current_user
from . import models
import functools

@contextlib.contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

def flash_form_errors(form):
	[flash("Invalid data in item '%s': %s" % (k,", ".join(v)), 'error')
		for k,v in form.errors.items()]

def require_user_role(role):
	def _wrap(func):
		@functools.wraps(func)
		def _wrapped(*a, **k):
			if models.ROLE_HIERARCHY.index(role)<=models.ROLE_HIERARCHY.index(current_user.role):
				return func(*a,**k)
			else:
				flash("You do not have the permission to access this", 'error')
				return redirect(url_for('home'))
		return _wrapped
	return _wrap