from flask import Flask
app = Flask(__name__)

miko="kaka"

@app.route("/api/python")
def hello_world():
    return miko