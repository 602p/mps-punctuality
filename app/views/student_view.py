from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import desc
from flask_login import login_required
import datetime

from .. import app, db
from .. import models
from .. import util
from .. import forms

@app.route('/student/<sid>')
@login_required
def student_view(sid):
	student=models.Student.query.filter_by(id=int(sid)).one()
	sevents=list(reversed(models.AttendanceEvent.query.filter_by(student_id=int(sid)).order_by(desc(models.AttendanceEvent.id)).all()))
	event_forms=[forms.EventForm(obj=e) for e in sevents]
	for i, e in enumerate(sevents):
		event_forms[i].time.data=e.time.strftime("%b %d %Y      %I:%M %p")
	return render_template("student_view.html", 
		student=student,
		sorted_events=sevents,
		assc_events=len(student.attendance_events),
		consequences_completed=all(e.consequence_status for e in student.attendance_events),
		reasons=models.Reason.query.all(),
		event_forms=event_forms)

@app.route('/redirect_from_sid_name', methods=['GET', 'POST'])
def student_view_wrapper():
	full_name, mid = models.Student.split_uid_name(request.form.get("student_uid_name"))
	student=models.Student.query.filter_by(full_name=full_name, marss_id=mid).first()
	return redirect(url_for("student_view", sid=student.id))

@app.route("/_edit_event/<sid>/<eid>", methods=['POST'])
@login_required
@util.require_user_role('edit')
def edit_event_inline_apply(sid, eid):
	sid,eid=int(sid),int(eid)
	form=forms.EventForm(request.form)
	if form.validate():
		event=models.AttendanceEvent.query.filter_by(id=eid).one()
		form.fill_to(event, exclude=['time'])
		event.time=datetime.datetime.strptime(form.time.data, "%b %d %Y      %I:%M %p")
		db.session.commit()
		flash("Updated event")
		return redirect(url_for("student_view", sid=sid))
	else:
		util.flash_form_errors(form)
		return redirect(url_for("student_view", sid=sid))