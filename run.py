"""The application."""
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_cors import CORS, cross_origin

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__, static_url_path='/static')
CORS(app)
app.config.from_object('config')
db = SQLAlchemy(app)