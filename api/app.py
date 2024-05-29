from flask import Flask, request
from syllable_splitter import split_input
import json

app = Flask(__name__)

@app.route("/api/python", methods=["POST"])
def german_syllable_splitter():
    request_data = request.get_json()
    input_data = request_data['input']
    
    syllables = split_input(input_data)
    
    syllables = json.dumps(syllables)
    
    return syllables

if __name__ == "__main__":
    app.run(debug=True)
