
import functools
from flask import request
from flask_login import current_user
from flask_socketio import disconnect, emit, join_room
from run import socketio

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


# SOCKET LOGIN

@socketio.on('join')
@authenticated_only
def handle_join():
    join_room(current_user.name)
    print(f"User {current_user.name} has joined")
    emit('join_ack', {'message': f'room {current_user.name} has been joined'})
