from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
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
    Handle any other API calls, run games, and return results for frontend download
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract player data
        player_a = data.get("playerA", {})
        player_b = data.get("playerB", {})
        
        # Extract data for run_games method
        playerA_variables = player_a.get("variables", [])
        playerA_scenarios = player_a.get("scenarioValues", [])
        playerA_equation = player_a.get("formula", "")
        
        playerB_variables = player_b.get("variables", [])
        playerB_scenarios = player_b.get("scenarioValues", [])
        playerB_equation = player_b.get("formula", "")
        
        # Run the games using your method
        playerA_data, playerB_data = run_games(
            playerA_variables, 
            playerA_scenarios, 
            playerA_equation, 
            playerB_variables, 
            playerB_scenarios, 
            playerB_equation
        )
        
        # Create results object
        results = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": subpath,
            "message": f"Games run successfully via endpoint '{subpath}'",
            "playerA_data": playerA_data,
            "playerB_data": playerB_data,
            "original_input": {
                "playerA": {
                    "variables": playerA_variables,
                    "scenarioValues": playerA_scenarios,
                    "formula": playerA_equation,
                    "scenarios": player_a.get("scenarios", [])
                },
                "playerB": {
                    "variables": playerB_variables,
                    "scenarioValues": playerB_scenarios,
                    "formula": playerB_equation,
                    "scenarios": player_b.get("scenarios", [])
                }
            }
        }
        
        # Return the results for frontend to download
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def run_games(playerA_variables, playerA_scenarios, playerA_equation, playerB_variables, playerB_scenarios, playerB_equation):
    # get variable data
    playerA_data = {}
    playerB_data = {} 

    for i in range(len(playerA_variables)):
        playerA_data[i] = {'max': playerA_variables[i]['max'], 
                           'min': playerA_variables[i]['min'], 
                           'stdev': playerA_variables[i]['stdev'], 
                           'weight': playerA_variables[i]['weight']}
      
  
    for i in range(len(playerB_variables)):
        playerB_data[i] = {'max': playerB_variables[i]['max'], 
                           'min': playerB_variables[i]['min'], 
                           'stdev': playerB_variables[i]['stdev'], 
                           'weight': playerB_variables[i]['weight']}

    
    # run formula on playerA variables 

    return playerA_data, playerB_data
    


