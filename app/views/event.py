from flask import render_template, redirect, url_for, request
import sqlalchemy, json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route('/create_event', methods=["GET", "POST"])
def create_event():
	if request.method=='POST':
		form=forms.EventForm(request.form)
		full_name, mid = models.Student.split_uid_name(form.student_uid_name.data)
		student=models.Student.query.filter_by(full_name=full_name, marss_id=mid).first()
		dateobj=datetime.datetime.strptime(form.time.data, "%Y/%m/%d %H:%M")
		event=models.AttendanceEvent(student.id, dateobj, form.comment.data)
		db.session.add(event)

		count=len(models.AttendanceEvent.query.filter_by(student_id=student.id).all())
		triggered=None
		for consequence in models.Consequence.query.all():
			if consequence.triggered(count):
				triggered=consequence
				break

		if triggered:
			event.consequence_id=triggered.id

		db.session.commit()
		return redirect(url_for("event_list"))
	else:
		form=forms.EventForm()
		return render_template("add_event.html", form=form)

@app.route('/events', methods=["GET", "POST"])
def event_list():
	return render_template("event_list.html", events=models.AttendanceEvent.query.all())

@app.route("/delete_event/<sid>")
def delete_event(sid):
	models.AttendanceEvent.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("event_list"))