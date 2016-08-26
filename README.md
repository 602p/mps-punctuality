# mps-punctuality

## Requirements
 * Python 3+
 * flask
 * flask-wtforms
 * flask-sqlalchemy
 * flask-admin
 * flask-oauthlib

## Usage

Set up database with `python tool.py createdb`
Seed sample students with `python tool.py seeddb`
Run server with `python run.py`

Get an OAuth key from google and select `Save as JSON` and save it as `instance/oauth.json`
I'd reccomend using an `/etc/hosts` entry to treat localhost as a website proper (e.g. `127.0.0.1 foobar.com`) and allowing that in the google control panel, otherwise it will ask you for offline access every time.