from flask import render_template, request, jsonify, send_from_directory
from run import db, app
from models import Chat, ChatMessage
import config
import json
import minesweeper

@app.route("/")
def hello():
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

if __name__ == "__main__":
    db.create_all()
    chat = Chat()
    db.session.add(chat)
    db.session.commit()
    app.run(host='0.0.0.0', port=config.PORT, debug=True, threaded=True)