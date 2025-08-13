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
        
        # Extract data from request
        playerA_variables = data.get('playerA_variables', [])
        playerA_scenarios = data.get('playerA_scenarios', [])
        playerA_equation = data.get('playerA_equation', '')
        playerB_variables = data.get('playerB_variables', [])
        playerB_scenarios = data.get('playerB_scenarios', [])
        playerB_equation = data.get('playerB_equation', '')
        
        # Run the games
        playerA_data, playerB_data = run_games(
            playerA_variables, playerA_scenarios, playerA_equation,
            playerB_variables, playerB_scenarios, playerB_equation
        )
        
        # Return JSON with simulation data
        return jsonify({
            'success': True,
            'playerA_data': playerA_data,
            'playerB_data': playerB_data,
            'message': 'Data generated successfully.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


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
    

