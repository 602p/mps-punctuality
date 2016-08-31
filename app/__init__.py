from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
 
app = Flask(__name__, static_url_path='/static')
with open("config.json", 'r') as fd:
	d=json.load(fd)
	print("config.json loaded -> "+str(d))
	app.config.update(d)
app.config['GOOGLE_ID'] = os.environ.get("GOOGLE_ID", '')
app.config['GOOGLE_SECRET'] = os.environ.get("GOOGLE_SECRET", '')
app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"]
app.config["SECRET_KEY"]=os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

db = SQLAlchemy(app)

from .views import student_view
from .views import backend
from .views import navigation
from .views import event
from .views import user

from . import admin

from . import oauth