from flask import Flask, redirect, url_for, session, request, jsonify, flash
from flask_oauthlib.client import OAuth
from flask_login import login_user
import json

from . import util
from . import app, db
from . import models
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/oauth_login')
def oauth_login():
    return google.authorize(callback=url_for('oauth_authorized', _external=True))

@app.route('/login/authorized')
def oauth_authorized():
    resp = google.authorized_response()
    if resp is None: #OAuth authorization failed
        flash("OAuth login failed: %s -> %s" %(request.args['error_reason'], request.args['error_description']))
        return redirect(url_for("home"))
    session['google_token'] = (resp['access_token'], '') #Stick it in the session (if we potentially decide to use
                                                         #more of Google's API features later, e.g. mailing or
                                                         #whatever we'll need this for the OAuth scope in the 
                                                         #API calls
    me = google.get('userinfo').data #Snarf out the user's free data
    user = models.User.query.filter_by(username=me["email"], auth_provider="OAUTH").first() #Is there a user with this
                                                                                            #email using OAuth already?
    if user: #If so...
        return util.try_login_user(user) #Proceed to try to log them in
    else: #Otherwise
        user=models.User( #Create a (disabled) account for them for the admin to enable later
            marss_id=-1,  #Cant find this w/o some kind of DB dump, if even applicable
            username=me["email"], #Google's return gaurenteed to have email, this is the username for OAuth accounts
            name=me["name"], #Google's return sometimes has name, otherwise empty string
            email=me["email"], #Store it here too
            auth_provider="OAUTH", #Use OAUTH provider, duh!
            enabled=False #And leave them disabled
        ) #Default permission='view'
        db.session.add(user)
        db.session.commit()
        flash("Please wait for an Administrator to enable your account")
        return redirect(url_for("login_user_page"))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')