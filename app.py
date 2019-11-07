from flask import Flask, render_template
from run import db, app

@app.route("/")
def hello():
    var = 12345
    return render_template(
        "index.html",
        to_show=var,
        )

@app.route("/game")
def gras():
    return "<b>TEST</b>"

@app.route("/api/homedata")
def api_data():
    print("ef")
    return "{'test': 42}"

# Chat



if __name__ == "__main__":
    db.create_all()
    app.run(port="5000", debug=True, threaded=True)