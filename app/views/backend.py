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
	return json.dumps([x.uid_name for x in 
		models.Student.query.filter(models.Student.full_name.contains(request.args.get("term"))).limit(10).all()])

@app.route("/_autocomplete_teacher", methods=['GET'])
@login_required
def autocomplete_teacher():
	return json.dumps([x.name for x in 
		models.Teacher.query.filter(models.Teacher.name.contains(request.args.get("term"))).limit(10).all()])

@app.route("/_add_event/<sid>", methods=['POST'])
@login_required
@util.require_user_role('edit')
def add_event(sid):
	dateobj=datetime.datetime.strptime(request.form.get("time"), "%b %d %Y      %I:%M %p")
	comment=request.form.get("comment")
	event=models.AttendanceEvent(int(sid), dateobj, models.Reason.query.filter_by(id=int(request.form.get("reason"))).one().text+
		(": " if comment else "")+comment)
	db.session.add(event)

	t=models.Teacher.query.filter_by(name=request.form.get("teacher")).first()
	if not t:
		flash("Invalid teacher", 'error')
		return redirect(url_for("student_view", sid=sid)) 
	event.teacher_id=t.id
	event.author_id=current_user.id

	count=len(models.AttendanceEvent.query.filter_by(student_id=int(sid)).all())
	triggered=None
	for consequence in models.Consequence.query.all():
		if consequence.triggered(count):
			triggered=consequence
			break

	if triggered:
		event.consequence_id=triggered.id
		if not triggered.has_consequence:
			event.consequence_status=True

	db.session.commit()
	flash("Event Added!")
	return redirect(url_for("student_view", sid=int(sid))+"#tardies")

@app.route("/_delete_event/<sid>/<eid>")
@login_required
@util.require_user_role('edit')
def delete_event(sid, eid):
	models.AttendanceEvent.query.filter_by(id=int(eid)).delete()
	db.session.commit()
	return redirect(url_for("student_view", sid=int(sid)))