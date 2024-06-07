from flask import render_template, jsonify

from servidor import app, api_blueprint

@app.route("/")
@app.route("/<path:_>")
def index(_=None):
    return render_template("index.html")

@api_blueprint.route("/ping")
def ping():
    return jsonify({"message": "pong"})

@api_blueprint.route("/user_contet" , methods=["GET"])
def user_content():
    return jsonify({"message": "user content"})

if __name__ == '__main__':
    app.run()