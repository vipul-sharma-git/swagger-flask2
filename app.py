""" Running an application instance """
from flask import render_template
import settings
import constants

# Create the application instance
CONNEX_APP = settings.connex_app

# Read the swagger.yml file to configure the endpoints
CONNEX_APP.add_api(constants.SWAGGER_FILE_NAME, arguments={"global": "global_value"})

# Create a URL route in our application for "/"
@CONNEX_APP.route("/")
def home():
    """
    :return: render home template file
    """
    return render_template("home.html")


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    CONNEX_APP.run(debug=True)
