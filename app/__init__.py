from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os
 
app = Flask(__name__, static_url_path='/static') #Create app. Simple static exposure
app.config['GOOGLE_ID'] = os.environ.get("GOOGLE_ID", '<disabled>') #Load from environment, falling back to empty string (app works without)
app.config['GOOGLE_SECRET'] = os.environ.get("GOOGLE_SECRET", '<disabled>') #Load from environment, falling back to empty string (app works without)
app.config["SQLALCHEMY_DATABASE_URI"]=os.environ["DATABASE_URL"] # #Load from environment, failing without
app.config["SECRET_KEY"]=os.environ.get("FLASK_SECRET_KEY", os.urandom(24)) #Try loading from env, generate if not found
                         # this is needed because on gunicorn running in multiprocess mode the randomly generated secrets
                         # will be different across processes/workers and therefor sessions will break. Also neccecary for
                         # a possible multi-dyno heroku implementation

db = SQLAlchemy(app)

from .views import student_view
from .views import backend
from .views import navigation
from .views import user

from . import admin

from . import oauth