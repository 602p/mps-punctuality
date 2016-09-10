from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import datetime
import os
from werkzeug.security import generate_password_hash, \
	 check_password_hash

ROLE_HIERARCHY=\
[
    'view', #Enter the application and view records
    'edit', #Create and modify records, students
    'admin' #Create and modify all data, edit server files, modify other users
]

class Period(db.Model):
	"""Records for tracking what period of the school day a date is whthin. All periods are queried for a certain date and
	the first to return true is displayed as the period of the event, else display -1."""
	__tablename__="periods"
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.Integer) #Period # (usually 0-7 inclusive)
	trigger = db.Column(db.String(200))  #Python snippet that runs on datetime objects

	def __init__(self, text=None, trigger=None):
		self.text=text
		self.trigger=trigger

	def triggered(self, date):
		"""Construct a namespace and return the result of executing the Period's snippet in it.
		WARNING: Potentially horifically unsafe if a bad admin has access to this"""
		ns={
		    "date":date, #Raw datetime object
		    "f":date.strftime, #Helper formatter reference
		    "m":(int(date.strftime("%H"))*60)+int(date.strftime("%M")) #Quasi-hack to get the minuite of the day. This is the preffered method. e.g. use `600<m<660` to match 10:00 to 11:00
		} 
		return eval(self.trigger, {}, ns) #Eval the snippet and return it

	@classmethod
	def get_for(cls, date):
		"""Helper class to get the period that matches a date"""
		for item in cls.query.all():
			if item.triggered(date):
				return item.number
		return -1

class Reason(db.Model):
	"""Simple text container. Root reason for an absence"""
	__tablename__="reasons"
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text)

	def __init__(self, text=None):
		self.text=text

class Teacher(db.Model):
	"""Simple text container. Teacher owning the class a tardy event occours in"""
	__tablename__="teachers"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))

	def __init__(self, name=None):
		self.name=name

	def __str__(self): return self.name

class User(db.Model):
	"""Application user model. Holds authentication data and some personal information."""
	__tablename__="users"
	id = db.Column(db.Integer, primary_key=True)
	marss_id = db.Column(db.Integer) #May be used if students are allowed to see their records
	enabled = db.Column(db.Boolean) #Only enabled users may log in. Prevents nobodys from registering/logging in with OAuth
	name = db.Column(db.String(100)) #User's name. Shown on Author fields
	username = db.Column(db.String(100)) #Username. Really only used internally. Arbitrary for LOCAL auth users, their Google email for OAUTH users
	session_token = db.Column(db.String(200)) #Random string. Flask-login session token. Change to invalidate sessions w/o changing their passowrd
	email = db.Column(db.String(100)) #Users' email. May be used later for alerts. Autofilled for OAUTH users.
	role = db.Column(db.String(100)) # 'view' 'edit' or 'admin'. See ROLE_HIERARCHY
	auth_provider = db.Column(db.String(10)) # 'LOCAL' or 'OAUTH'. LOCAL -> Use password_hash and app-local auth. OAUTH -> Use username as email to authenticate against google OAuth
	password_hash = db.Column(db.String(200)) # for LOCAL auth, the result of the werkzeug-provided password hashing function

	def __init__(self, marss_id=None, username=None, name=None, email=None, auth_provider=None, enabled=False, role="view"):
		self.marss_id=marss_id
		self.username=username
		self.name=name
		self.email=email
		self.enabled=enabled
		self.auth_provider=auth_provider
		self.role=role
		self.generate_session_token()

	@classmethod
	def empty(cls):
		"""Create a 'empty' instance of this for use with SQLForm"""
		return cls(0,'','','','LOCAL',False)

	def generate_session_token(self):
		"""(Re)Generate the user's session token. This will invalidate the user's session if they are logged in when done"""
		self.session_token=str(os.urandom(50)) #Get some random crap for the session token

	def set_password(self, plaintext):
		"""Set a new password from plaintext (hashed internally)"""
		self.password_hash=generate_password_hash(plaintext)

	def check_password(self, plaintext):
		"""Check a user's password form plaintext (hashed internally)"""
		return check_password_hash(self.password_hash, plaintext)

	def has_permission(self, role):
		return ROLE_HIERARCHY.index(self.role)>=ROLE_HIERARCHY.index(role)

	@property
	def is_authenticated(self):
		"""Is the user authenticated. For flask-admin"""
		return True
 
	@property
	def is_active(self):
		"""Is the user 'active'. Who knows what this means. For flask-admin"""
		return True
 
	@property
	def is_anonymous(self):
		"""Is the user a real. For flask-admin"""
		return False
 
	def get_id(self):
		"""Helper for flask-login"""
		return self.session_token

class Student(db.Model):
	"""Data holder class for Students who are associated with AttendanceEvents. Probably won't need to be modified once imported (other than comment)"""
	__tablename__="students"
	id = db.Column(db.Integer, primary_key=True)
	marss_id = db.Column(db.Integer, unique=True)
	first_name = db.Column(db.String(100))
	last_name = db.Column(db.String(100))
	pref_first_name = db.Column(db.String(100)) #Normally same as first_name.
	grade = db.Column(db.Integer) #Should be 9-12 inclusive, otherwise can't be filtered correctly (although thats just a UI matter, trivial to change)
	status = db.Column(db.String(100)) #'active' or 'inactive'. Not currently used other than a filter
	image = db.Column(db.String(100)) #URL in future. Unused currently
	phonedata = db.Column(db.Text) #Comment field
	comment = db.Column(db.Text) #Comment field

	def __init__(self, marss_id=None, first_name=None, last_name=None, pref_first_name=None, grade=9, status="active", image="<NOIMAGE>", phonedata="", comment=""):
		self.marss_id=marss_id
		self.first_name=first_name
		self.last_name=last_name
		self.pref_first_name=pref_first_name if pref_first_name is not None else first_name #If no preffered name specified, use first name
		self.grade=grade
		self.status=status
		self.image=image
		self.phonedata=phonedata
		self.comment=comment

	@classmethod
	def empty(cls):
		"""Create an 'empty' instance. For use with SQLForm"""
		return cls(-1, "","",None,-1)

	@hybrid_property
	def full_name(self):
		"""Students pretty full name"""
		return self.first_name+" "+self.last_name

	@property
	def uid_name(self):
		"""Students human-readable uniquely identifying name. Used in AutoComplete"""
		return self.first_name+" "+self.last_name+" ("+str(self.marss_id)+")"

	@property
	def unresolved_events(self):
		"""Does the student have any AttendanceEvents that are not resolved?"""
		return len([e for e in self.attendance_events if not e.consequences_completed])

	@classmethod
	def split_uid_name(cls, name):
		"""Turn a uid_name back into a full_name and marss_id"""
		return [name.split(" (")[0], int(name.split(" (")[1][:-1])]

	def __repr__(self):
		return '<Student %r>' % (self.first_name+self.last_name)

class AttendanceEvent(db.Model):
	"""Mutable event associated with a student, author user, time, teacher, period, reason, consequence and containing status and comment.
	Meat n' taters."""
	__tablename__="attendanceevents"
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id')) #Student event is associated with
	student = db.relationship('Student',
		backref=db.backref('attendance_events', lazy='joined'),
		foreign_keys="AttendanceEvent.student_id")
	time = db.Column(db.DateTime) #Time of the event
	consequence_id = db.Column(db.Integer, db.ForeignKey('consequences.id')) #Consequence triggered by this event
	consequence = db.relationship('Consequence', foreign_keys="AttendanceEvent.consequence_id", backref=db.backref('attendance_events', lazy='joined'))
	consequence_status = db.Column(db.Text) #Status of the consequence. Comma-seperated 'True'/'False' values corresponding to the clauses (lines) of the consequence
	comment = db.Column(db.Text) #Comment. Ought to be prefixed with <Reason>:
	author_id = db.Column(db.Integer, db.ForeignKey('users.id')) #Last user to edit (or create) the event
	author = db.relationship('User', foreign_keys="AttendanceEvent.author_id")
	teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id')) #Teacher the event is associated with
	teacher = db.relationship('Teacher', foreign_keys="AttendanceEvent.teacher_id")

	def __init__(self, student_id=None, time=None, comment=None):
		self.student_id=student_id
		self.time=time
		self.comment=comment
		self.consequence_status="False"

	@classmethod
	def empty(cls):
		"""Create an 'empty' instance. For use with SQLForm"""
		return cls(-1,datetime.datetime.now(),"")

	@property
	def period(self):
		"""Get the period that this event's time falls within"""
		return Period.get_for(self.time)

	@property
	def _consequene_status_elements(self):
		"""Helper for getting the string values of consequence statuses"""
		return [eval(v) for v in self.consequence_status.split(",")] #Simple Eval

	@property
	def consequence_statuses(self):
		"""Get the logical status (that is, if there is no consequence marked in the Consequence record all is well) of the event"""
		if not self.consequence.has_consequence:
			return [True for _ in self._consequene_status_elements] #If there is no logical consequence, return all is well
		return self._consequene_status_elements #Return the stored values

	@consequence_statuses.setter
	def consequence_statuses(self, val):
		"""Set the consequence statuses, taking a list of booleans"""
		self.consequence_status=",".join(str(x) for x in val)

	@property
	def consequences_completed(self):
		"""Have all consequence lines for this event been logically completed"""
		return all(self.consequence_statuses)

	def __repr__(self):
		return "<AttendanceEvent %r: %r>" % (self.id, self.time)

class Consequence(db.Model):
	"""Action records that apply themselves to AttendanceEvents"""
	__tablename__="consequences"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30)) #Fancy name.
	description = db.Column(db.Text) #Description text. Each line produces an independant checkbox
	trigger = db.Column(db.String(100)) #python snippet run against a number of tardies 
	                                    #(including the tardy it is being run from)
	                                    #to determine if this consequence applies:
	                                    #return a boolean, only one consequence should return True
	                                    #for any integer value of n, if this is not so
	                                    #the first (by database ID) will be applied
	has_consequence=db.Column(db.Boolean) #Does this logically have a consequence? That is: should it
	                                      #be considered completed the moment it is applied or does
	                                      #it need to be checked off by the proctor

	def __init__(self, name=None, description=None, trigger=None, has_consequence=False):
		self.description=description
		self.trigger=trigger
		self.name=name
		self.has_consequence=has_consequence

	@classmethod
	def empty(cls):
		"""Create an 'empty' instance. For use with SQLForm"""
		return cls("","","",False)

	@property
	def description_lines(self):
		"""Description as an array of lines (each will have a status associated with it)"""
		return self.description.split("\n")

	def __repr__(self):
		return "<Consequence %r: %r -> %r [%r]>" % (self.name, self.trigger, self.description, str(self.has_consequence))

	def triggered(self, num_tardies):
		"""Exec the snippet on num_tardies (in the snippet namespace this is `n`) and return the value"""
		return eval(self.trigger, {}, {"n":num_tardies})