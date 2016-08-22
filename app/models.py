from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import datetime

class Student(db.Model):
	__tablename__="students"
	id = db.Column(db.Integer, primary_key=True)
	marss_id = db.Column(db.Integer, unique=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	pref_first_name = db.Column(db.String(100))
	grade = db.Column(db.Integer)
	status = db.Column(db.String(100))
	image = db.Column(db.String(100))
	phonedata = db.Column(db.Text)
	comment = db.Column(db.Text)

	def __init__(self, marss_id, first_name, last_name, pref_first_name=None, grade=9, status="active", image="<NOIMAGE>", phonedata="", comment=""):
		self.marss_id=marss_id
		self.first_name=first_name
		self.last_name=last_name
		self.pref_first_name=pref_first_name if pref_first_name is not None else first_name
		self.grade=grade
		self.status=status
		self.image=image
		self.phonedata=phonedata
		self.comment=comment

	@classmethod
	def empty(cls):
		return cls(-1, "","",None,-1)

	@hybrid_property
	def full_name(self):
		return self.first_name+" "+self.last_name

	@property
	def uid_name(self):
		return self.first_name+" "+self.last_name+" ("+str(self.marss_id)+")"

	@property
	def unresolved_events(self):
		return len([e for e in self.attendance_events if not e.consequence_status])

	@classmethod
	def split_uid_name(cls, name):
		return [name.split(" (")[0], int(name.split(" (")[1][:-1])]

	def __repr__(self):
		return '<Student %r>' % (self.first_name+self.last_name)

class AttendanceEvent(db.Model):
	__tablename__="attendanceevents"
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	student = db.relationship('Student',
		backref=db.backref('attendance_events', lazy='joined'),
		foreign_keys="AttendanceEvent.student_id")
	time = db.Column(db.DateTime)
	consequence_id = db.Column(db.Integer, db.ForeignKey('consequences.id'))
	consequence = db.relationship('Consequence', foreign_keys="AttendanceEvent.consequence_id", backref=db.backref('attendance_events', lazy='joined'))
	consequence_status = db.Column(db.Boolean)
	comment = db.Column(db.Text)

	def __init__(self, student_id, time, comment):
		self.student_id=student_id
		self.time=time
		self.comment=comment
		self.consequence_status=False

	@classmethod
	def empty(cls):
		return cls(-1,datetime.datetime.now(),"")

	def __repr__(self):
		return "<AttendanceEvent %r: %r>" % (self.id, self.time)

class Consequence(db.Model):
	__tablename__="consequences"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	description = db.Column(db.Text)
	trigger = db.Column(db.String(100))
	has_consequence=db.Column(db.Boolean)

	def __init__(self, name, description, trigger, has_consequence):
		self.description=description
		self.trigger=trigger
		self.name=name
		self.has_consequence=has_consequence

	@classmethod
	def empty(cls):
		return cls("","","",False)

	def __repr__(self):
		return "<Consequence %r: %r -> %r [%r]>" % (self.name, self.trigger, self.description, str(self.has_consequence))

	def triggered(self, num_tardies):
		return eval(self.trigger, {}, {"n":num_tardies})