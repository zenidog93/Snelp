from flask_app import app


#!!!!!!!! Always import controllers. Controllers handle the routes in your project!
from flask_app.controllers import user_routes, ride_routes


if __name__ == "__main__":
    app.run(debug=True)