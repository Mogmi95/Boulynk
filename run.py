"""The application."""
from flask_sqlalchemy import SQLAlchemy
import flask
from flask_cors import CORS, cross_origin
from flask_login import LoginManager
from flask_socketio import SocketIO

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__, static_url_path='/static')
CORS(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object('config')
db = SQLAlchemy(app)