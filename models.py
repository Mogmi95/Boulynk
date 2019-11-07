from sqlalchemy.sql import func

from .app import db

class Chat(db.Model):
    """
    Describe a Chat.
    """
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    messages = None # TODO

class ChatMessage(db.Model):
    """
    Describe a single message.
    """
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, default="")
    author = db.Column(db.String, default="Anon")
    timestamp = db.Column(db.DateTime, unique=False, server_default=func.now())
