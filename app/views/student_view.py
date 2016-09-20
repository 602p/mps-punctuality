from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import desc
from flask_login import login_required, current_user
import datetime

from .. import app, db
from .. import models
from .. import util
from .. import forms

@app.route('/student/<sid>')
@login_required
def student_view(sid):
	student=models.Student.query.filter_by(id=int(sid)).one() #Grab the student by sid
	sevents=list(reversed(#In reverse (that is, added) order
		models.AttendanceEvent.query.filter_by(student_id=int(sid)) #grab events associated with this student
		.order_by(desc(models.AttendanceEvent.id)).all() #Sort by ID, functionally insertion order
	))
	event_forms=[forms.EventForm(obj=e) for e in sevents] #Build a set of Forms for these events
	for i, e in enumerate(sevents):
		event_forms[i].time.data=e.time.strftime("%b %d %Y      %I:%M %p") #Update time with correct format
	return render_template("student_view.html", 
		student=student,
		sorted_events=sevents,
		assc_events=len(student.attendance_events),
		consequences_completed=all(e.consequences_completed for e in student.attendance_events),
		reasons=models.Reason.query.all(),
		event_forms=event_forms)

@app.route('/redirect_from_sid_name', methods=['GET', 'POST'])
def student_view_wrapper():
	"""Redirect to a student view given a sid_name from autocomlete"""
	try:
		full_name, mid = models.Student.split_uid_name(request.args.get("student_uid_name"))
	except (IndexError, ValueError):
		flash("Please select a student from the dropdown list", 'error')
		return redirect(url_for('home'))
	student=models.Student.query.filter_by(full_name=full_name, marss_id=mid).first()
	if not student:
		flash("Please select a student from the dropdown list", 'error')
		return redirect(url_for('home'))
	return redirect(url_for("student_view", sid=student.id))

@app.route("/_edit_event/<sid>/<eid>", methods=['POST'])
@login_required
@util.require_user_role('edit')
def edit_event_inline_apply(sid, eid):
	"""Apply an inline edit form"""
	sid,eid=int(sid),int(eid)
	form=forms.EventForm(request.form)
	if form.validate():
		event=models.AttendanceEvent.query.filter_by(id=eid).one() #eid from form target
		form.fill_to(event, exclude=['time', 'teacher', 'consequence_status']) #Exclude special data
		statuses=[]
		for i, _ in enumerate(event.consequence.description_lines):
			statuses.append(bool(request.form.get("line_%d" % i,""))) #Build a array of status booleans
		event.consequence_statuses=statuses #Update statuses
		try:
			event.time=datetime.datetime.strptime(form.time.data, "%b %d %Y      %I:%M %p") #Parse datetime
		except ValueError: #Catch invalid times
			flash("Invalid Date/Time", 'error')
			return redirect(url_for("student_view", sid=sid))
		t=models.Teacher.query.filter_by(name=form.teacher.data).first() #Grab the teacher
		if not t: #Make sure they exist
			flash("Invalid teacher", 'error')
			return redirect(url_for("student_view", sid=sid)) 
		event.teacher_id=t.id #Set the teacher
		event.author_id=current_user.id #Update author to current user
		db.session.commit()
		flash("Updated event")
		return redirect(url_for("student_view", sid=sid)+"#tardies")
	else:
		util.flash_form_errors(form)
		return redirect(url_for("student_view", sid=sid)+"#tardies")