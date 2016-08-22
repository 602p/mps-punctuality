from flask import render_template, redirect, url_for, request
import sqlalchemy, json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route('/edit_event/<sid>/<eid>', methods=["GET", "POST"])
def edit_event(sid, eid):
	sid, eid = int(sid), int(eid)
	if request.method=="POST":
		event=models.AttendanceEvent.query.filter_by(id=eid).one()
		event.time=datetime.datetime.strptime(request.form.get("time"), "%Y/%m/%d %H:%M")
		event.comment=request.form.get("comment")
		event.consequence_status=bool(request.form.get("consequence_status"))
		db.session.add(event)
		db.session.commit()
		return redirect(url_for('student_view', sid=sid))
	if request.method=="GET":
		return render_template("edit_event.html", event=models.AttendanceEvent.query.filter_by(id=eid).one(), sid=sid)