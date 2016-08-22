from flask import render_template, request, redirect, url_for

from .. import app, db
from .. import models

@app.route('/student/<sid>')
def student_view(sid):
	student=models.Student.query.filter_by(id=int(sid)).one()
	return render_template("student_view.html", 
		student=student,
		assc_events=len(student.attendance_events),
		consequences_completed=all(e.consequence_status for e in student.attendance_events))

@app.route('/redirect_from_sid_name', methods=['GET', 'POST'])
def student_view_wrapper():
	full_name, mid = models.Student.split_uid_name(request.form.get("student_uid_name"))
	student=models.Student.query.filter_by(full_name=full_name, marss_id=mid).first()
	return redirect(url_for("student_view", sid=student.id))