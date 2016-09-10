from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SelectField, Field, BooleanField
from wtforms.validators import DataRequired

class SQLForm(Form):
	"""Handy dandy form mixin for filling to-and-from SQLAlchemy model instances"""
	def fill_from(self, record):
		for item, value in self.__dict__.items():
			if isinstance(value, Field) and item!="csrf_token":
				getattr(self, item).data = getattr(record, item)

	def fill_to(self, record, exclude=[]):
		for item, value in self.__dict__.items():
			if isinstance(value, Field) and item!="csrf_token" and item not in exclude:
				setattr(record, item, value.data)

class EventForm(SQLForm):
	time = StringField("Time", validators=[DataRequired()])
	comment = TextAreaField("Reason")
	consequence_status = BooleanField("consequence_completed")
	teacher=StringField("Teacher")
	id=IntegerField("internal_id")
