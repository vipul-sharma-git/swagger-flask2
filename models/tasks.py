""" Asynchronous Jobs Table """
from settings import db


class Task(db.Model):
    """Tasks table"""

    __tablename__ = "tasks1"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(32), unique=True)
    task_status = db.Column(db.String(32))
    task_error = db.Column(db.String(64))
