from flask import render_template, redirect, url_for, request
import sqlalchemy

from .. import app, db
from .. import models
from .. import forms

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
				mode="Create"
			else:
				mode="Update"
				form.fill_to(models.Student.query.filter_by(id=sid).one())
			try:
				db.session.commit()
			except BaseException as e:
				return render_template("create_student.html", form=form, error=str(e), mode=mode)
			return "Success"#redirect(url_for("student_list"))
		else:
			return render_template("create_student.html", form=form, error="Invalid Form Data -> "+str(form.errors), mode=mode)
	else:
		form=forms.StudentForm()
		try:
			form.fill_from(models.Student.query.filter_by(id=sid).one())
			mode="Update"
		except sqlalchemy.orm.exc.NoResultFound:
			mode="Create"
		return render_template("create_student.html", form=form, error=None, mode=mode) 