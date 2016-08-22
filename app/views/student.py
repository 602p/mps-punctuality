from flask import render_template, redirect, url_for, request
import sqlalchemy

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route('/create_student', methods=["GET", "POST"])
def create_student():
	return edit_internal(-1)

@app.route('/edit_student/<sid>', methods=["GET", "POST"])
def edit_student(sid):
	print(request.args)
	return edit_internal(sid)

def edit_internal(sid):
	print(request.args)
	sid=int(sid)
	mode="Create" if sid==-1 else "Update"
	if request.method=="POST":
		form = forms.StudentForm(request.form)

		if form.validate():
			if sid==-1:
				db.session.add(models.Student(
					form.marss_id.data,
					form.first_name.data,
					form.last_name.data,
					form.pref_first_name.data if form.pref_first_name.data is not "" else None,
					form.grade.data,
					form.status.data,
					None,
					form.phonedata.data,
					form.comment.data
				))
				
			else:
				form.fill_to(models.Student.query.filter_by(id=sid).one())
			try:
				db.session.commit()
			except BaseException as e:
				return render_template("create_student.html", form=form, error=str(e), mode=mode)
			return redirect(url_for("student_list"))
		else:
			return render_template("create_student.html", form=form, error="Invalid Form Data -> "+str(form.errors), mode=mode)
	else:
		form=forms.StudentForm()
		with util.ignored(sqlalchemy.orm.exc.NoResultFound):
			form.fill_from(models.Student.query.filter_by(id=sid).one())
		return render_template("create_student.html", form=form, error=None, mode=mode) 

@app.route("/students")
def student_list():
	result=models.Student.query
	for k,v in request.args.items():
		with util.ignored(AttributeError):
			result=result.filter(getattr(models.Student, k).contains(v))
	return render_template("student_list.html", students=result.all())

@app.route("/delete_student/<sid>")
def delete_student(sid):
	models.Student.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("student_list"))