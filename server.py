import json
from flask import Flask, jsonify

app = Flask(__name__)
intents = json.loads(open('intents.json').read())

@app.route('/')
def index():
    return "Welcome to our project API"

@app.route("/intents", methods=['GET'])
def get():
    return jsonify(intents)

if __name__ == "__main__":
    app.run()