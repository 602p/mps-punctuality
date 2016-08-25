from . import models
from . import app, db

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import current_user
from flask import flash, redirect, url_for

class SecureView(ModelView):
	def is_accessible(self):
		if not 'role' in current_user.__dict__: return False
		return current_user.role=="admin"

	def inaccessible_callback(self, name, **kwargs):
		flash("Woah nelly! You aren't an admin!", 'error')
		return redirect(url_for("home"))

class UserView(SecureView):
	form_choices = {
	    'role': [
	        ('view', 'View Only'),
	        ('edit', 'Edit AttendanceEvents'),
	        ('admin', 'Access this interface')
	    ]
	}
	column_exclude_list = ['session_token', 'password_hash']

admin = Admin(app, name='mps-punctuality', template_mode='bootstrap3')
admin.add_view(UserView(models.User, db.session))
admin.add_view(SecureView(models.Student, db.session))
admin.add_view(SecureView(models.AttendanceEvent, db.session))
admin.add_view(SecureView(models.Consequence, db.session))
admin.add_view(SecureView(models.Reason, db.session))
admin.add_view(SecureView(models.Period, db.session))
admin.add_view(SecureView(models.Teacher, db.session))