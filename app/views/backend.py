from flask import render_template, redirect, url_for, request, flash
import json, datetime
from flask_login import login_required, current_user

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route("/_autocomplete_student", methods=['GET'])
@login_required
def autocomplete_student():
	return json.dumps([
		x.uid_name for x in #Returns names
		models.Student.query.filter(
			models.Student.full_name.ilike("%"+request.args.get("term")+"%") #Case insensitive contains
		).limit(10).all() #Get only 10
	])

@app.route("/_autocomplete_teacher", methods=['GET'])
@login_required
def autocomplete_teacher():
	return json.dumps([
		x.name for x in #Return names
		models.Teacher.query.filter(
			models.Teacher.name.ilike("%"+request.args.get("term")+"%") #Case insensitive contains
		).limit(10).all() #Get only 10
	])

@app.route("/_add_event/<sid>", methods=['POST'])
@login_required
@util.require_user_role('edit')
def add_event(sid):
	"""Add an event and redirect to the user with id <sid>"""
	try:
		dateobj=datetime.datetime.strptime(request.form.get("time"), "%b %d %Y      %I:%M %p") #Same format as JS
	except ValueError:
		flash("Invalid Date/Time!", 'error')
		return redirect(url_for("student_view", sid=int(sid)))
	comment=request.form.get("comment")
	event=models.AttendanceEvent(int(sid), dateobj, 
		models.Reason.query.filter_by(id=int(request.form.get("reason"))).one().text+ #Grab out the reason text they selected
		(": " if comment else "")+comment) #Include comment if applicable
	

	t=models.Teacher.query.filter_by(name=request.form.get("teacher")).first() #Grab the teacher they entered
	if not t:
		flash("Invalid teacher", 'error') #Spit them out if it's invalid
		return redirect(url_for("student_view", sid=sid)) 
	event.teacher_id=t.id #Mark the teacher
	event.author_id=current_user.id #Mark the editor as current user

	count=len(models.AttendanceEvent.query.filter_by(student_id=int(sid)).all())+1 #How many tardies (including this) does the student have?
	triggered=None
	for consequence in models.Consequence.query.all():
		if consequence.triggered(count): #If the consequence triggers, break
			triggered=consequence
			break

	if triggered:
		event.consequence_id=triggered.id #Mark the consequence
		if not triggered.has_consequence:
			event.consequence_status="True" #If there is no logical consequence, mark it as completed

	db.session.add(event) #Do this last in case a validation step fails

	db.session.commit()
	flash("Event Added!")
	return redirect(url_for("student_view", sid=int(sid))+"#tardies")

@app.route("/_delete_event/<sid>/<eid>")
@login_required
@util.require_user_role('edit')
def delete_event(sid, eid):
	"""Get rid of the event with id <eid> and return to student <sid>"""
	models.AttendanceEvent.query.filter_by(id=int(eid)).delete()
	db.session.commit()
	return redirect(url_for("student_view", sid=int(sid)))