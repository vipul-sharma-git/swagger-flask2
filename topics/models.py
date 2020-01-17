# listed topics tables
from config import db
from datetime import datetime


class Topics(db.Model):
   __tablename__ = "topics"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32))
   categories = db.Column(db.String(32))
   timestamp = db.Column(
       db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
   )
