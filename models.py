from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import json
import random

from run import db

# LOGIN

class User(db.Model):
    """
    Describe an user.
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    # Flask-Login integration
    def is_authenticated(self):
        """Check if the user is authenticated."""
        return True

    def is_active(self):
        """Check if the user is active."""
        return True

    def is_anonymous(self):
        """Check if the user is anonymous."""
        return False

    def get_id(self):
        """Get the user's ID."""
        return self.id

    def __unicode__(self):
        """Required for administrative interface."""
        return str(self.name)

# CHAT

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

# CODENAMES

class CodenamesGame(db.Model):
    """
    Describe a game of Codenames.
    """
    id = db.Column(db.Integer, primary_key=True)
    # List of all the words stored as JSON
    _words = db.Column(db.String, default="[]")
    # List of the correct words (True if correct, False if not) stored as JSON
    _correct_words = db.Column(db.String, default="[]")
    # Status of the words : 0 is unchecked, 1 is correct, -1 is incorrect
    _words_status = db.Column(db.String, default="[]")
    current_player = None
    current_clue = None
    status = None

    @property
    def words(self):
        return json.loads(self._words)

    @words.setter
    def words(self, value):
        self._words = json.dumps(value)

    @property
    def correct_words(self):
        return json.loads(self._correct_words)

    @correct_words.setter
    def correct_words(self, value):
        self._correct_words = json.dumps(value)

    @property
    def words_status(self):
        return json.loads(self._words_status)

    @words_status.setter
    def words_status(self, value):
        self._words_status = json.dumps(value)

    def __init__(self, words, player):
        self.words = words
        random.shuffle(self.words)
        self.correct_words = list([False] * 15 + [True] * 10)
        random.shuffle(self.correct_words)
        self.words_status = list([0] * 25)
        self.current_player = player
        current_clue = None

    def get_public_board(self):
        result = []
        for i in range(len(self.words)):
            item = {}
            item['word'] = self.words[i]
            item['status'] = self.words_status[i]
            result.append(item)
        return result

    def get_whole_board(self):
        result = []
        for i in range(len(self.words)):
            item = {}
            item['word'] = self.words[i]
            item['status'] = self.words_status[i]
            result.append(item)
        return result