from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
 
app = Flask(__name__, static_url_path='/static')
with open("config.json", 'r') as fd:
	d=json.load(fd)
	print("config.json loaded -> "+str(d))
	app.config.update(d)
app.config["SECRET_KEY"]=os.urandom(24)

db = SQLAlchemy(app)

from . import admin

