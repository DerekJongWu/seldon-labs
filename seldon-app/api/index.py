from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
from sl_package.sampling import sample_from_distribution
import numpy as np
import pandas as pd
from io import BytesIO
from flask import send_file

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
        df_a = player_data_to_df(playerA_data)
        df_b = player_data_to_df(playerB_data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_a.to_excel(writer, index=False, sheet_name='PlayerA')
            df_b.to_excel(writer, index=False, sheet_name='PlayerB')
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='game_results.xlsx'
        )
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


def run_games(playerA_variables, playerA_scenarios, playerA_equation, playerB_variables, playerB_scenarios, playerB_equation, num_samples=1000):
    def process_player(variables, scenario_values, equation, num_samples):
        variable_means = get_variable_means_per_scenario(variables, scenario_values)
        scenario_results = []
        for scenario_idx, scenario in enumerate(scenario_values):
            samples = []
            for _ in range(num_samples):
                sampled = {}
                normalized = {}
                for var_idx, var in enumerate(variables):
                    var_name = var.get('name', f'var_{var_idx}')
                    mean = scenario[var_idx]
                    stdev = var['stdev']
                    min_val = var['min']
                    max_val = var['max']
                    sign = var.get('sign', 1)  # default to positive if not specified

                    # 1. Sample from distribution
                    val = sample_from_distribution(mean, stdev)

                    # 2. Normalize
                    if max_val == min_val:
                        norm = 0.0  # Avoid division by zero
                    elif sign == 1:
                        norm = (val - min_val) / (max_val - min_val)
                    else:
                        norm = (max_val - val) / (max_val - min_val)
                    norm = max(0, min(1, norm))

                    sampled[var_name] = val
                    normalized[var_name] = norm

                # 3. Evaluate equation
                try:
                    result = eval(equation, {"__builtins__": None}, normalized)
                except Exception as e:
                    result = None

                samples.append({
                    "sampled": sampled,
                    "normalized": normalized,
                    "result": result
                })
            scenario_results.append(samples)
        return scenario_results

    playerA_data = process_player(playerA_variables, playerA_scenarios, playerA_equation, num_samples)
    playerB_data = process_player(playerB_variables, playerB_scenarios, playerB_equation, num_samples)
    return playerA_data, playerB_data
    

def get_variable_means_per_scenario(variables, scenario_values):
    """
    Returns a dict mapping variable names to a list of their mean values per scenario.
    variables: list of dicts, each with at least a 'name' key
    scenario_values: list of lists, each inner list is the means for all variables in one scenario
    """
    result = {}
    for var_idx, var in enumerate(variables):
        var_name = var.get('name', f'var_{var_idx}')
        # Collect the mean for this variable across all scenarios
        means = [scenario[var_idx] for scenario in scenario_values]
        result[var_name] = means
    return result

def player_data_to_df(player_data):
    rows = []
    for scenario_idx, samples in enumerate(player_data):
        for sample_idx, sample in enumerate(samples):
            row = {
                "scenario": scenario_idx,
                "sample": sample_idx,
                **{f"sampled_{k}": v for k, v in sample["sampled"].items()},
                **{f"normalized_{k}": v for k, v in sample["normalized"].items()},
                "result": sample["result"]
            }
            rows.append(row)
    return pd.DataFrame(rows)
    

