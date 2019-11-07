from flask import Flask, render_template
from run import db, app
import config

@app.route("/")
def hello():
    var = 12345
    return render_template(
        "index.html",
        to_show=var,
        )

@app.route("/size/<size>")
def api_search(size):
    print(size)
    return "succes"

@app.route("/games/demineur")
def demineur():

    return render_template(
        "demineur.html",
    )


# Chat



if __name__ == "__main__":
    db.create_all()
    app.run(port=config.PORT, debug=True, threaded=True)