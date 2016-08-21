from . import db

class Student(db.Model):
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

	def __repr__(self):
		return '<Student %r>' % (self.first_name+self.last_name)

class AttendaceEvent(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	student = db.relationship('Student',
		backref=db.backref('attendance_events', lazy='dynamic'))
	time = db.Column(db.DateTime)
	consequence_id = db.Column(db.Integer, db.ForeignKey('student.id'))
	consequence = db.relationship('Consequence')
	consequence_status = db.Column(db.Boolean)
	comment = db.Column(db.Text)

	def __init__(self, student_id, time, comment):
		self.student_id=student_id
		self.time=time
		self.comment=comment
		self.consequence_status=False

	def __repr__(self):
		return "<AttendaceEvent %r: %r>" % self.id, self.time

class Consequence(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	description = db.Column(db.Text)
	trigger = db.Column(db.String(100))

	def __init__(self, name, description, trigger):
		self.description=description
		self.trigger=trigger
		self.name=name

	def __repr__(self):
		return "<Consequence %r -> %r>" % self.trigger, self.description

	def triggered(self, num_tardies):
		return eval(self.trigger, {}, {"n":num_tardies})