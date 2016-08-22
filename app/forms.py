from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SelectField, Field, BooleanField
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
	student_uid_name = StringField("Student", id="student_uid_name", validators=[DataRequired()])
	time = StringField("Time", validators=[DataRequired()])
	comment = TextAreaField("Comment")

class ConsequenceForm(SQLForm):
	name = StringField("Name", validators=[DataRequired()])
	description = TextAreaField("Description")
	trigger = StringField("Trigger", validators=[DataRequired()])
	has_consequence = BooleanField("Has Consequence")