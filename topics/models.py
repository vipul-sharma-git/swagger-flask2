"""listed topics tables"""

from datetime import datetime
from settings import db


class Topics(db.Model):
    """Topics table"""

    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    categories = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
