from flask import render_template
import settings
import constants

# Create the application instance
connex_app = settings.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api(constants.SWAGGER_FILE_NAME)

# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    return render_template("home.html")


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    # connex_app.run(host="127.0.0.1", port=5000, debug=True)
    connex_app.run(host="0.0.0.0", debug=True)
