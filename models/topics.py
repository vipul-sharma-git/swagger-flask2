"""listed topics tables"""

from datetime import datetime
from sqlalchemy.orm import relationship
from settings import db


class Topics(db.Model):
    """Topics table"""

    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    categories = relationship("Categories", cascade="all,delete")
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Categories(db.Model):
    """Categories table"""

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    topic_name = db.Column(db.Integer, db.ForeignKey("topics.id"))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
