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
	"""Only allow admin users to view the View and redirect non-admins home with a chastizement"""
	def is_accessible(self):
		if not 'role' in current_user.__dict__: return False #That is, if they're the default flask-admin user
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
	def index(self): #Redirect user to users table if they somehow end up here
		return redirect('/admin/user')

admin = Admin(app, name='mps-punctuality',
	template_mode='bootstrap3', #fancy shmancy lookin page
	base_template="admin_base.html", #custom template to hide the big ol inactive name button
	index_view=HomeView(menu_class_name="hidden")) #Hack to hide home link
admin.add_view(UserView(models.User, db.session)) #Subclass to show special text for roles, and hide garbo text

#Model Views->
admin.add_view(SecureView(models.Student, db.session))
admin.add_view(SecureView(models.AttendanceEvent, db.session))
admin.add_view(SecureView(models.Consequence, db.session))
admin.add_view(SecureView(models.Reason, db.session))
admin.add_view(SecureView(models.Period, db.session))
admin.add_view(SecureView(models.Teacher, db.session))

path = os.path.dirname(__file__)
admin.add_view(SecureFileAdmin(path, '/', name='Files'))

admin.add_link(MenuLink(name='BACK TO SITE', category='', url='/'))  #Per D.G.
admin.add_link(MenuLink(name='LOG OUT', category='', url='/logout')) #Per D.G.