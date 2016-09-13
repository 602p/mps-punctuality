from flask import render_template, redirect, url_for, request
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
				result=result.filter(getattr(models.Student, k).contains(v))
				
	students=result.all()
	if request.args.get("meta_unresolved"):
		students=[s for s in students if (s.unresolved_events>0 if request.args.get("meta_unresolved")=="yes" else s.unresolved_events==0)]
	if request.args.get("meta_tardies_more"):
		students=[s for s in students if len(s.attendance_events)>int(request.args.get("meta_tardies_more"))]
	if request.args.get("meta_tardies_less"):
		students=[s for s in students if len(s.attendance_events)<int(request.args.get("meta_tardies_less"))]
	return render_template("overview.html", students=students)