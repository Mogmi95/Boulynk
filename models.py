from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from run import db


class Chat(db.Model):
    """
    Describe a Chat.
    """
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    messages = relationship('ChatMessage', backref='chat')
    chat_id = Column(Integer, ForeignKey('chat.id'))


class ChatMessage(db.Model):
    """
    Describe a single message.
    """
    __tablename__ = 'chat_message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, default='')
    author = db.Column(db.String, default='Anon')
    timestamp = db.Column(db.DateTime, unique=False, server_default=func.now())
    # Foreign elements
    chat_id = Column(Integer, ForeignKey('chat.id'))

    def __init__(self, message, author):
        """Simple constructor."""
        self.content = message
        self.author = author

    def __repr__(self):
        """Simple log method."""
        return str(self.author + " " + self.content)