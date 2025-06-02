from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.get_json()
    # Here you would process the data and run your game logic
    return 'hello world'