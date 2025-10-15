from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract player data from request
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


