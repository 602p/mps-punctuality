from flask import render_template, redirect, url_for, request
import sqlalchemy, json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route('/debug/create_consequence', methods=["GET", "POST"])
def d_create_consequence():
	return d_edit_consequence(-1)

@app.route('/debug/edit_consequence/<sid>', methods=["GET", "POST"])
def d_edit_consequence(sid):
	sid=int(sid)
	mode = "Create" if sid == -1 else "Edit"
	if request.method=='POST':
		form=forms.ConsequenceForm(request.form)
		if form.validate():
			if sid == -1:
				consequence = models.Consequence.empty()
				form.fill_to(consequence)
				db.session.add(consequence)
			else:
				form.fill_to(models.Consequence.query.filter_by(id=sid).one())
			db.session.commit()
			return redirect(url_for("d_consequence_list"))
		else:
			return render_template("debug/create_consequence.html", form=form, error="Invalid Form Data -> "+str(form.errors), mode=mode)
	else:
		form=forms.ConsequenceForm()
		with util.ignored(sqlalchemy.orm.exc.NoResultFound):
			form.fill_from(models.Consequence.query.filter_by(id=sid).one())
		return render_template("debug/create_consequence.html", form=form, error=None, mode=mode)

@app.route('/debug/consequences', methods=["GET", "POST"])
def d_consequence_list():
	return render_template("debug/consequence_list.html", consequences=models.Consequence.query.all())

@app.route("/debug/delete_consequence/<sid>")
def d_delete_consequence(sid):
	models.Consequence.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("d_consequence_list"))

@app.route('/debug/create_event', methods=["GET", "POST"])
def d_create_event():
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
		return redirect(url_for("d_event_list"))
	else:
		form=forms.EventForm()
		return render_template("debug/add_event.html", form=form)

@app.route('/debug/events', methods=["GET", "POST"])
def d_event_list():
	return render_template("debug/event_list.html", events=models.AttendanceEvent.query.all())

@app.route("/debug/delete_event/<sid>")
def d_delete_event(sid):
	models.AttendanceEvent.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("d_event_list"))

@app.route('/debug/create_student', methods=["GET", "POST"])
def d_create_student():
	return d_edit_student(-1)

@app.route('/debug/edit_student/<sid>', methods=["GET", "POST"])
def d_edit_student(sid):
	sid=int(sid)
	mode="Create" if sid==-1 else "Update"
	if request.method=="POST":
		form = forms.StudentForm(request.form)
		if form.validate():
			if sid==-1:
				student=models.Student.empty()
				form.fill_to(student)
				db.session.add(student)
			else:
				student=models.Student.query.filter_by(id=sid).one()
				form.fill_to(student)
			if student.pref_first_name=="":student.pref_first_name=student.first_name
			try:
				db.session.commit()
			except BaseException as e:
				return render_template("debug/create_student.html", form=form, error=str(e), mode=mode)
			return redirect(url_for("d_student_list"))
		else:
			return render_template("debug/create_student.html", form=form, error="Invalid Form Data -> "+str(form.errors), mode=mode)
	else:
		form=forms.StudentForm()
		with util.ignored(sqlalchemy.orm.exc.NoResultFound):
			form.fill_from(models.Student.query.filter_by(id=sid).one())
		return render_template("debug/create_student.html", form=form, error=None, mode=mode) 

@app.route("/debug/students")
def d_student_list():
	result=models.Student.query
	for k,v in request.args.items():
		with util.ignored(AttributeError):
			result=result.filter(getattr(models.Student, k).contains(v))
	return render_template("debug/student_list.html", students=result.all())

@app.route("/debug/delete_student/<sid>")
def d_delete_student(sid):
	models.Student.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("d_student_list"))

@app.route("/debug/autocomplete_student", methods=['GET'])
def d_autocomplete_student():
	return json.dumps([x.uid_name for x in 
		models.Student.query.filter(models.Student.full_name.contains(request.args.get("term"))).limit(10).all()])