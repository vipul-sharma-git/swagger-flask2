""" Project Configuration values """
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DB_FILENAME = "topics_data.db"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Build the Sqlite ULR for SqlAlchemy
SQLITE_URL = "sqlite:///" + os.path.join(BASEDIR, DB_FILENAME)
