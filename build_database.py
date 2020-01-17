# import os
from config import db
from topics.models import Topics
from asyncworker.models import Task

# Create the database
db.create_all()


p = Topics(name="python", categories="ok 1,ok 2")
db.session.add(p)
db.session.commit()
p = Topics(name="go", categories="ok 1,ok 2")
db.session.add(p)
db.session.commit()
p = Topics(name="c", categories="ok 1,ok 2")
db.session.add(p)
db.session.commit()
