from flask import render_template, redirect, url_for, request
import json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route("/_autocomplete_student", methods=['GET'])
def autocomplete_student():
	return json.dumps([x.uid_name for x in 
		models.Student.query.filter(models.Student.full_name.contains(request.args.get("term"))).limit(10).all()])

@app.route("/_add_event/<sid>", methods=['POST'])
def add_event(sid):
	dateobj=datetime.datetime.strptime(request.form.get("time"), "%Y/%m/%d %H:%M")
	event=models.AttendanceEvent(int(sid), dateobj, request.form.get("comment"))
	db.session.add(event)

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
	return redirect(url_for("student_view", sid=int(sid)))

@app.route("/_delete_event/<sid>/<eid>")
def delete_event(sid, eid):
	models.AttendanceEvent.query.filter_by(id=int(eid)).delete()
	db.session.commit()
	return redirect(url_for("student_view", sid=int(sid)))