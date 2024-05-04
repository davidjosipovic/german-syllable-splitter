from flask import Flask
from compound_split import char_split
from spylls.hunspell import Dictionary
app = Flask(__name__)





@app.route("/api/python")
def hello_world():
    return 2