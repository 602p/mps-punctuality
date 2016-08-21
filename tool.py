import app, sys
import app.models

if sys.argv[1]=="createdb":
	app.db.create_all()