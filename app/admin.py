from . import models
from . import app, db

from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask import flash, redirect, url_for
import os

class SecureMixin(object):

	def is_accessible(self):
		if not 'role' in current_user.__dict__: return False
		return current_user.role=="admin"

	def inaccessible_callback(self, name, **kwargs):
		flash("Woah nelly! You aren't an admin!", 'error')
		return redirect(url_for("home"))

class SecureView(SecureMixin, ModelView):pass

class SecureFileAdmin(SecureMixin, FileAdmin):pass

class UserView(SecureMixin, ModelView):
	form_choices = {
		'role': [
			('view', 'View Only'),
			('edit', 'Edit AttendanceEvents'),
			('admin', 'Access this interface')
		]
	}
	column_exclude_list = ['session_token', 'password_hash']

class HomeView(SecureMixin, AdminIndexView):
	@expose('/')
	def index(self):
		return redirect('/admin/user')

admin = Admin(app, name='mps-punctuality', template_mode='bootstrap3', base_template="admin_base.html",
	index_view=HomeView(menu_class_name="hidden"))
admin.add_view(UserView(models.User, db.session))
admin.add_view(SecureView(models.Student, db.session))
admin.add_view(SecureView(models.AttendanceEvent, db.session))
admin.add_view(SecureView(models.Consequence, db.session))
admin.add_view(SecureView(models.Reason, db.session))
admin.add_view(SecureView(models.Period, db.session))
admin.add_view(SecureView(models.Teacher, db.session))

path = os.path.dirname(__file__)
admin.add_view(SecureFileAdmin(path, '/', name='Files'))

admin.add_link(MenuLink(name='BACK TO SITE', category='', url='/'))
admin.add_link(MenuLink(name='LOG OUT', category='', url='/'))