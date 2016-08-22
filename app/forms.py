from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SelectField, Field
from wtforms.validators import DataRequired

class SQLForm(Form):
	def fill_from(self, record):
		for item, value in self.__dict__.items():
			if isinstance(value, Field) and item!="csrf_token":
				getattr(self, item).data = getattr(record, item)

	def fill_to(self, record):
		for item, value in self.__dict__.items():
			if isinstance(value, Field) and item!="csrf_token":
				setattr(record, item, value.data)

class StudentForm(SQLForm):
	marss_id = IntegerField('Student ID', validators=[DataRequired()])
	first_name = StringField('First Name', validators=[DataRequired()])
	pref_first_name = StringField('Preffered First Name')
	last_name = StringField('Last Name', validators=[DataRequired()])
	grade = IntegerField('Current Grade', validators=[DataRequired()])
	status = SelectField('School Status', choices=[('active', 'Active'), ('inactive', 'Inactive')])
	phonedata = TextAreaField("Phone Info")
	comment = TextAreaField("Comment")

class EventForm(SQLForm):
	student = IntegerField("Student ID", validators=[DataRequired()])
	time = StringField("Time", validators=[DataRequired()])