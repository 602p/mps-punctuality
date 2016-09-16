from flask import render_template, redirect, url_for, request, flash
import sqlalchemy, json, datetime
from flask_login import login_required, current_user

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route("/")
@login_required
def home():
	return render_template("logged_in_landing.html", user=current_user)

@app.route('/overview')
@login_required
def overview():
	result=models.Student.query
	for k,v in request.args.items():
		with util.ignored(AttributeError):
			if k=="status" and v!="":
				result=result.filter_by(status=v)
			elif v!="":
				if v.isdecimal():
					result=result.filter(getattr(models.Student, k)==v)
				else:
					result=result.filter(getattr(models.Student, k).contains(v))
				
	students=result.all()
	if request.args.get("meta_unresolved"):
		students=[s for s in students if (s.unresolved_events>0 if request.args.get("meta_unresolved")=="yes" else s.unresolved_events==0)]
	if request.args.get("meta_tardies_more"):
		students=[s for s in students if len(s.attendance_events)>int(request.args.get("meta_tardies_more"))]
	if request.args.get("meta_tardies_less"):
		students=[s for s in students if len(s.attendance_events)<int(request.args.get("meta_tardies_less"))]

	if len(students)==0:
		flash("Your search returned no students", 'error')
		return redirect(url_for('home'))
	if len(students)==1:
		flash("Your search returned only one student. You have been redirected to their page")
		return redirect(url_for('student_view', sid=students[0].id))
	return render_template("overview.html", students=students)