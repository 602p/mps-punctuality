from flask import render_template, redirect, url_for, request
import sqlalchemy, json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route('/create_consequence', methods=["GET", "POST"])
def create_consequence():
	return edit_consequence(-1)

@app.route('/edit_consequence/<sid>', methods=["GET", "POST"])
def edit_consequence(sid):
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
			return redirect(url_for("consequence_list"))
		else:
			return render_template("create_consequence.html", form=form, error="Invalid Form Data -> "+str(form.errors), mode=mode)
	else:
		form=forms.ConsequenceForm()
		with util.ignored(sqlalchemy.orm.exc.NoResultFound):
			form.fill_from(models.Consequence.query.filter_by(id=sid).one())
		return render_template("create_consequence.html", form=form, error=None, mode=mode)

@app.route('/consequences', methods=["GET", "POST"])
def consequence_list():
	return render_template("consequence_list.html", consequences=models.Consequence.query.all())

@app.route("/delete_consequence/<sid>")
def delete_consequence(sid):
	models.Consequence.query.filter_by(id=int(sid)).delete()
	db.session.commit()
	return redirect(url_for("consequence_list"))