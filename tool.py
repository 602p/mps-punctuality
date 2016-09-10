"""tool.py

Simple tooling for interacting with the DB.

USAGE:
	python tool.py createdb 		- Create the DataBase tables
	python tool.py resetdb			- Drop all DataBase tables
	python tool.py seeddb [num]		- Seed the database with default values, including [num] students. Default=20
							Also creates the user localadmin with password `admin`
	python -i tool.py 				- Do nothing, so as to allow you to interact with the DB thru the python REPL"""
import app, sys
import app.models
import random
from names import TEST_NAMES, TEST_TEACHERS, TEST_REASONS, TEST_CONSQUENCES

if len(sys.argv)==1 and not sys.flags.interactive:
	print(__doc__)
	sys.exit()

if sys.flags.interactive:
	print("             ===INTERACTIVE MODE===")
	print("Models -> app.models.*")
	print("DB -> app.db")
	print("**REMEMBER TO COMMIT WITH `app.db.session.commit()`**")
elif sys.argv[1]=="createdb":
	app.db.create_all()
elif sys.argv[1]=="resetdb":
	app.db.drop_all()
	app.db.create_all()
elif sys.argv[1]=="seeddb":
	for n, name in enumerate(TEST_NAMES[:int(sys.argv[2] if len(sys.argv)>2 else 20)]): #Seed students, defaulting to 20
		print("Adding Name #%02d -> %s" % (n, name))
		app.db.session.add(app.models.Student(
					random.randint(100000, 999999), #Random MARSS ID
					name.split(" ")[0], #First Name
					name.split(" ")[1], #Last Name
					None, #No pref. first name
					random.randint(9,12), #Random Grade
					random.choice(["active","inactive"]), #Random Status
					None, #No Image
					"", #Empty phonedata
					"" #Empty comment
				))
	for n, name in enumerate(TEST_TEACHERS): #Seed teachers
		print("Adding Teacher #%02d -> %s" %(n, name))
		app.db.session.add(app.models.Teacher(name))
	for n, name in enumerate(TEST_REASONS): #Seed reasons
		print("Adding Reason #%02d -> %s" %(n, name))
		app.db.session.add(app.models.Reason(name))
	for n, d in enumerate(TEST_CONSQUENCES): #Seed consequences
		print("Adding consquence #%02d -> %s" %(n, str(d)))
		app.db.session.add(app.models.Consequence(**d))
	print("Adding localadmin user. Password=admin")
	localadmin=app.models.User(-1, #Placeholder MARSS ID
		'localadmin', #username 'localadmin'
		'localadmin', #name
		'', #no email
		'LOCAL', #local (duh!) auth
		True, #Enable it immeaditley
		'admin' #And make it an admin so they can sort out their own users
	)
	localadmin.set_password("admin") #Set the password to 'admin' WARNING: Change this once app is up and running!
	app.db.session.add(localadmin)
	app.db.session.commit()