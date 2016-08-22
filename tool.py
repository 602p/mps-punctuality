import app, sys
import app.models
import random
from names import TEST_NAMES

if sys.argv[1]=="createdb":
	app.db.create_all()
if sys.argv[1]=="resetdb":
	app.db.drop_all()
	app.db.create_all()
if sys.argv[1]=="seeddb":
	for n, name in enumerate(TEST_NAMES[:int(sys.argv[2] if len(sys.argv)>2 else 20)]):
		print("Adding Name #%02d -> %s" % (n, name))
		app.db.session.add(app.models.Student(
					random.randint(100000, 999999),
					name.split(" ")[0],
					name.split(" ")[1],
					None,
					random.randint(9,12),
					random.choice(["active","inactive"]),
					None,
					"",
					""
				))
		app.db.session.commit()