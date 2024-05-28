from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    with open('emotion_results.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
