from flask import render_template, redirect, url_for, request
import sqlalchemy, json, datetime

from .. import app, db
from .. import models
from .. import forms
from .. import util

@app.route("/")
def home():
	return render_template("logged_in_landing.html")