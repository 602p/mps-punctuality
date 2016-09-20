# mps-punctuality

## Usage

Install PostgresSQL, and set environment var DATABASE_URL to its URI (e.g. postgres://username:password@url/database)
Create a VirtualEnv and install modules from requirements.txt (`python -m pip install -r requirements.txt`)
Set up database with `python tool.py createdb`
Seed sample students with `python tool.py seeddb`
Run server with `python run.py`

(Optional) Get an OAuth key from google and set GOOGLE_ID and GOOGLE_SECRET to your OAuth ID and Secret respectivley
I'd reccomend using an `/etc/hosts` entry to treat localhost as a website proper (e.g. `127.0.0.1 foobar.com`) and allowing that in the google control panel, otherwise it will ask you for offline access every time.