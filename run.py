"""The application."""
from flask_sqlalchemy import SQLAlchemy
import flask

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__, static_url_path='/static')
#app.config.from_object('config')
db = SQLAlchemy(app)