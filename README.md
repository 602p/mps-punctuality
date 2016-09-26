# mps-punctuality

## Usage

 * Install PostgresSQL, and set environment var DATABASE_URL to its URI (e.g. postgres://username:password@url/database)
 * Create a VirtualEnv and install modules from requirements.txt (`python -m pip install -r requirements.txt`)
 * Set up database with `python tool.py createdb` (This will create a local admin account with username/password localadmin/admin)
 * Seed sample students with `python tool.py seeddb`
 * (Optional) Get an OAuth key from google and set GOOGLE_ID and GOOGLE_SECRET to your OAuth ID and Secret respectivley
   * I'd reccomend using an `/etc/hosts` entry to treat localhost as a website proper (e.g. `127.0.0.1 foobar.com`) and allowing that in the google control panel, otherwise it will ask you for offline access every time.
 * (Optional) Set FLASK_DEBUG=1 to see failure traces
 * Run server with `python startserver.py`

## Deployment

 * MAKE SURE `FLASK_DEBUG` is set to 0, otherwise you'll have a massive security hole
 * (Optional, but reccomended) Set up Gunicorn/Apache/NGINX to run as a frontend server
   * If your server of choice will spawn multiple WSGI workers (gunicorn, probably others) set `FLASK_SECRET_KEY` to some random text as a crypto seed across the workers, otherwise you will have intermittent session behavior
   * Gunicorn is listed in requirements.txt so you should have it installed already, run with `gunicorn app:app`
 * IMPORTANT: Remove/Change localadmin to something more secure
 * Run server thru a scheduler/rc as needed, your good to go
   * Student/Staff import can be done thru `python -im tool` to get an interactive app python shell, and use CSV or a tool of you choice to create ORM objects and publish them to the DB. Don't try to do this while the app is running, it'll probably break
