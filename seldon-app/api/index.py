from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.get_json()
    # Here you would process the data and run your game logic
    return 'hello world'

@app.route("/api/generate", methods=["POST"])
def generate():
    """
    Handle the generate button click and return player input data in JSON format
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract player data
        player_a = data.get("playerA", {})
        player_b = data.get("playerB", {})
        
        # Format the response with all player inputs
        response = {
            "message": "Player input data received successfully",
            "timestamp": datetime.now().isoformat(),
            "playerA": {
                "variables": player_a.get("variables", []),
                "scenarioValues": player_a.get("scenarioValues", []),
                "formula": player_a.get("formula", ""),
                "scenarios": player_a.get("scenarios", [])
            },
            "playerB": {
                "variables": player_b.get("variables", []),
                "scenarioValues": player_b.get("scenarioValues", []),
                "formula": player_b.get("formula", ""),
                "scenarios": player_b.get("scenarios", [])
            },
            "summary": {
                "totalVariablesPlayerA": len(player_a.get("variables", [])),
                "totalVariablesPlayerB": len(player_b.get("variables", [])),
                "scenariosCount": len(player_a.get("scenarios", [])),
                "playerAHasFormula": bool(player_a.get("formula")),
                "playerBHasFormula": bool(player_b.get("formula"))
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Catch-all route for any other API calls
@app.route("/api/<path:subpath>", methods=["POST"])
def handle_api_calls(subpath):
    """
    Handle any other API calls and return the data in JSON format
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract player data
        player_a = data.get("playerA", {})
        player_b = data.get("playerB", {})
        
        # Format the response with all player inputs
        response = {
            "message": f"API endpoint '{subpath}' called successfully",
            "endpoint": subpath,
            "timestamp": datetime.now().isoformat(),
            "playerA": {
                "variables": player_a.get("variables", []),
                "scenarioValues": player_a.get("scenarioValues", []),
                "formula": player_a.get("formula", ""),
                "scenarios": player_a.get("scenarios", [])
            },
            "playerB": {
                "variables": player_b.get("variables", []),
                "scenarioValues": player_b.get("scenarioValues", []),
                "formula": player_b.get("formula", ""),
                "scenarios": player_b.get("scenarios", [])
            },
            "summary": {
                "totalVariablesPlayerA": len(player_a.get("variables", [])),
                "totalVariablesPlayerB": len(player_b.get("variables", [])),
                "scenariosCount": len(player_a.get("scenarios", [])),
                "playerAHasFormula": bool(player_a.get("formula")),
                "playerBHasFormula": bool(player_b.get("formula"))
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500