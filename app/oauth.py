from flask import Flask, redirect, url_for, session, request, jsonify, flash
from flask_oauthlib.client import OAuth
from flask_login import login_user
import json

from . import authentication
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
    if resp is None:
        flash("OAuth login failed: %s -> %s" %(request.args['error_reason'], request.args['error_description']))
        return redirect(url_for("home"))
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo').data
    user = models.User.query.filter_by(username=me["email"], auth_provider="OAUTH").first()
    if user:
        return authentication.try_login_user(user)
    else:
        user=models.User(
            marss_id=-1,
            username=me["email"],
            name=me["name"],
            email=me["email"],
            auth_provider="OAUTH",
            enabled=False
        )
        db.session.add(user)
        db.session.commit()
        flash("Please wait for an Administrator to enable your account")
        return redirect(url_for("login_user_page"))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')