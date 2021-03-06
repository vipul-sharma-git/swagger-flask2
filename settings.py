""" Project setting """
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import config
import constants

# Create the connexion application instance
connex_app = connexion.App(
    __name__, specification_dir=config.BASEDIR, arguments={"global": "global_value"},
)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SqlAlchemy part of the app instance
app.config[constants.SQLALCHEMY_ECHO_KEY] = config.SQLALCHEMY_ECHO
app.config[constants.SQLALCHEMY_DATABASE_URI_KEY] = config.SQLITE_URL
app.config[
    constants.SQLALCHEMY_TRACK_MODIFICATIONS_KEY
] = config.SQLALCHEMY_TRACK_MODIFICATIONS

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
