from flask import render_template

from .. import app

@app.route('/')
def logged_in_landing():
	return render_template("logged_in_landing.html")