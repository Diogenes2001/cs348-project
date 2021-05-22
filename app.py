import json
from flask import Flask, request, json, jsonify
from flask_cors import CORS

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/test")
def test():
    return jsonify("Success!")

if __name__ == "main":
    app.run()