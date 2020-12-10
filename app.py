from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin
from trips import trip
from users import users
import models
import os
from flask_login import LoginManager

DEBUG = True
PORT = 8000

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
# @cross_origin()

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None'
)

app.secret_key = "This is the secret key. Here it is."

login_manager = LoginManager()

login_manager.init_app(app)



# CORS(app, supports_credentials = True)
CORS(trip, origins=['http://localhost:3000', 'https://www.bing.com', 'https://trip-planner-map-react.herokuapp.com/'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000', 'https://www.bing.com', 'https://trip-planner-map-react.herokuapp.com/'], supports_credentials=True)



app.register_blueprint(trip, url_prefix='/api/v1/trips')
app.register_blueprint(users, url_prefix='/api/v1/users')
@cross_origin()

@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user
        # should return None not raise an exception if the ID is not valid
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
	return "Hello"

@app.route('/sayhi/<username>')
def hello(username):
	return "Hello {}".format(username)

if 'ON_HEROKU' in os.environ:
  print('\non heroku!')
  models.initialize()

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)
