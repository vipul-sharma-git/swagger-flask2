""" Create tables in DB"""
# import os
from settings import db

# Create the database
db.create_all()
