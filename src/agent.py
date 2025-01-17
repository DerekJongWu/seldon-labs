import numpy as np
from scipy.optimize import minimize
from typing import List, Tuple, Callable, Optional
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from itertools import product

class EmpiricalGame:
    def __init__(self, num_players: int, strategy_space: List[float]):
        """
        Initialize an empirical game.
        
        Args:
            num_players: Number of players in the game
            strategy_space: List of available strategies (can be discrete or continuous)
        """
        self.num_players = num_players
        self.strategy_space = strategy_space
        self.payoff_data = {}  # Store empirical payoff observations
        self.learned_payoff_function = None
    
    def add_observation(self, profile: Tuple[float, ...], payoffs: List[float]):
        """
        Add an empirical observation of payoffs for a strategy profile.
        
        Args:
            profile: Tuple of strategies played
            payoffs: List of payoffs received by each player
        """
        if len(profile) != self.num_players or len(payoffs) != self.num_players:
            raise ValueError("Profile and payoffs must match number of players")
        
        self.payoff_data[profile] = payoffs
    
    def learn_payoff_function(self, degree: int = 2):
        """
        Learn a polynomial payoff function from empirical data.
        
        Args:
            degree: Degree of polynomial to fit
        """
        X = np.array([list(profile) for profile in self.payoff_data.keys()])
        y = np.array([payoffs[0] for payoffs in self.payoff_data.values()])
        
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        def learned_payoff(profile):
            return model.predict(poly.transform([profile]))[0]
        
        self.learned_payoff_function = learned_payoff
        return learned_payoff

    def best_response(self, other_strategies: List[float]) -> float:
        """
        Find best response to other players' strategies.
        
        Args:
            other_strategies: List of strategies played by other players
            
        Returns:
            Best response strategy
        """
        if not self.learned_payoff_function:
            raise ValueError("Must learn payoff function before computing best response")
        
        def negative_payoff(strategy):
            profile = [strategy] + other_strategies
            return -self.learned_payoff_function(profile)
        
        result = minimize(negative_payoff, x0=0.5, bounds=[(0, 1)])
        return result.x[0]

    def find_pure_nash_equilibrium(self, tolerance: float = 1e-5) -> Optional[List[float]]:
        """
        Find a pure strategy Nash equilibrium using best response dynamics.
        
        Args:
            tolerance: Convergence tolerance
            
        Returns:
            List of strategies forming a pure Nash equilibrium, or None if not found
        """
        current_profile = [0.5] * self.num_players
        
        for _ in range(100):  # Max iterations
            new_profile = []
            max_change = 0
            
            for i in range(self.num_players):
                other_strategies = current_profile[:i] + current_profile[i+1:]
                best_resp = self.best_response(other_strategies)
                new_profile.append(best_resp)
                max_change = max(max_change, abs(best_resp - current_profile[i]))
            
            if max_change < tolerance:
                return new_profile
                
            current_profile = new_profile
            
        return None

    def compute_epsilon(self, profile: List[float]) -> float:
        """
        Compute epsilon (maximum gain from deviation) for a strategy profile.
        
        Args:
            profile: Strategy profile to evaluate
            
        Returns:
            Epsilon value
        """
        max_gain = 0
        
        for i in range(self.num_players):
            other_strategies = profile[:i] + profile[i+1:]
            best_resp = self.best_response(other_strategies)
            
            # Current payoff
            current_payoff = self.learned_payoff_function(profile)
            
            # Best response payoff
            best_profile = profile[:i] + [best_resp] + profile[i+1:]
            best_payoff = self.learned_payoff_function(best_profile)
            
            gain = best_payoff - current_payoff
            max_gain = max(max_gain, gain)
            
        return max_gain

class SymmetricGame(EmpiricalGame):
    """Extension for symmetric games with additional optimization."""
    
    def aggregate_other_strategies(self, profile: List[float], player: int) -> Tuple[float, float]:
        """
        Aggregate other players' strategies for symmetric games.
        
        Args:
            profile: Full strategy profile
            player: Player index
            
        Returns:
            Tuple of (sum, sum of squares) of other players' strategies
        """
        other_strategies = profile[:player] + profile[player+1:]
        return (sum(other_strategies), sum(s*s for s in other_strategies))

    def learn_symmetric_payoff_function(self, degree: int = 2):
        """
        Learn a symmetric polynomial payoff function.
        """
        X = []
        y = []
        
        for profile, payoffs in self.payoff_data.items():
            for i in range(self.num_players):
                strategy = profile[i]
                agg_sum, agg_square = self.aggregate_other_strategies(list(profile), i)
                X.append([strategy, agg_sum, agg_square])
                y.append(payoffs[i])
        
        X = np.array(X)
        y = np.array(y)
        
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        def learned_payoff(profile):
            strategy = profile[0]
            agg_sum, agg_square = self.aggregate_other_strategies(profile, 0)
            return model.predict(poly.transform([[strategy, agg_sum, agg_square]]))[0]
        
        self.learned_payoff_function = learned_payoff
        return learned_payoff

def run_simulation_example():
    """Example usage of the framework."""
    # Create a symmetric game with 2 players
    game = SymmetricGame(num_players=2, strategy_space=[i/10 for i in range(11)])
    
    # Generate some synthetic data (first-price auction example)
    def true_payoff(profile):
        s1, s2 = profile[0], profile[1]
        if s1 >= s2:
            return (s1-1)*((s2**2) - 3*(s1**2))/(6*(s1**2)) if s1 > 0 else 0.25
        return s1*(1-s1)/(3*s2) if s2 > 0 else 0.25
    
    # Add observations
    strategies = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    for s1, s2 in product(strategies, repeat=2):
        payoff1 = true_payoff([s1, s2])
        payoff2 = true_payoff([s2, s1])
        game.add_observation((s1, s2), [payoff1, payoff2])
    
    # Learn payoff function
    game.learn_symmetric_payoff_function(degree=2)
    
    # Find equilibrium
    eq = game.find_pure_nash_equilibrium()
    if eq:
        print(f"Found pure Nash equilibrium: {eq}")
        print(f"Epsilon: {game.compute_epsilon(eq)}")
    
    return game

# Example usage
if __name__ == "__main__":
    print(1)
    game = run_simulation_example()