import flask

app = flask.Flask(__name__)

app.get("/")(lambda: "API is running!")
