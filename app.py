from flask import Flask, render_template
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(port="5000", debug=True, threaded=True)