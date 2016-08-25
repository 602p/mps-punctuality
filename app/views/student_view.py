from flask import render_template, request, redirect, url_for
from sqlalchemy import desc
from flask_login import login_required

from .. import app, db
from .. import models

@app.route('/student/<sid>')
@login_required
def student_view(sid):
	student=models.Student.query.filter_by(id=int(sid)).one()
	sevents=list(reversed(models.AttendanceEvent.query.filter_by(student_id=int(sid)).order_by(desc(models.AttendanceEvent.id)).all()))
	return render_template("student_view.html", 
		student=student,
		sorted_events=sevents,
		assc_events=len(student.attendance_events),
		consequences_completed=all(e.consequence_status for e in student.attendance_events))

@app.route('/redirect_from_sid_name', methods=['GET', 'POST'])
def student_view_wrapper():
	full_name, mid = models.Student.split_uid_name(request.form.get("student_uid_name"))
	student=models.Student.query.filter_by(full_name=full_name, marss_id=mid).first()
	return redirect(url_for("student_view", sid=student.id))