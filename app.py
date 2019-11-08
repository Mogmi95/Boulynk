from flask import render_template, request, jsonify, send_from_directory, flash, request, abort, redirect, url_for
from wtforms import form, fields, validators
from flask_login import login_required, login_user, logout_user
from run import db, app, login_manager
from models import User, Chat, ChatMessage, CodenamesGame
import config
import json
import minesweeper

# LOGIN

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/login", defaults={'user_id': None}, methods=["GET", "POST"])
@app.route('/login/<user_id>', methods=['GET', 'POST'])
def login(user_id=None):
    if user_id is not None:
        user = User.query.filter_by(name=user_id).first()
        if user is None:
            flash("NO")
            return render_template('login.html')
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('index'))
    flash("NO")
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# COMMON ROUTES

@app.route("/")
@login_required
def index():
    var = 12345
    return render_template(
        "index.html",
        to_show=var,
        )

@app.route('/files/<path:path>')
def send_file(path):
    return send_from_directory('templates', path)

@app.route("/games/demineur")
def demineur():
    return render_template(
        "demineur.html",
    )

@app.route("/api/homedata")
def api_data():
    print("ef")
    return "{'test': 42}"

# Chat
@app.route("/chat")
def show_chat():
    chat = Chat.query.first()
    return render_template('chat.html', chat=chat)

@app.route("/chat/api/add", methods=["POST"])
def api_add_chat_message():
    data = json.loads(request.data)
    add_chat_message(data["message"], data["author"])
    return "OK"

def add_chat_message(message, author):
    chat = Chat.query.first()
    chat.messages.append(ChatMessage(message, author))
    db.session.commit()

# Codenames

@app.route("/game/codenames")
def show_codenames():
    # Get game or None if none available
    # TODO How to get who is playing
    codename_game = CodenamesGame(
        ["banana", "apple", "pizza"],
        "LYON"
    )

    return render_template(
        "codenames.html",
        board=codename_game.get_public_board()
    )

@app.route("/game/codenames/api/submit/<id>")
def api_codenames_submit(id):
    game = CodenamesGame.query.first()
    game.submit(id)
    game.status
    return game.get_public_board()

@app.route("/game/codenames/api/clue/<clue>")
def api_codenames_give_clue(clue):
    return "OK"

if __name__ == "__main__":
    db.create_all()
    chat = Chat()
    db.session.add(chat)

    lyon = User("lyon")
    paris = User("paris")
    db.session.add(lyon)
    db.session.add(paris)

    db.session.commit()
    app.run(host='0.0.0.0', port=config.PORT, debug=True, threaded=True)