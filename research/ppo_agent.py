import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
import matplotlib.pyplot as plt

class TariffEnv(gym.Env):
    """
    Multi-agent reinforcement learning environment for tariff competition.
    """
    def __init__(self, num_countries=2):
        super(TariffEnv, self).__init__()
        
        self.num_countries = num_countries
        self.action_space = spaces.MultiDiscrete([11] * num_countries)  # Tariff levels from 0% to 10%
        self.observation_space = spaces.Box(low=0, high=1, shape=(num_countries,), dtype=np.float32)  # Trade balances
        
        self.trade_flows = np.ones(num_countries)  # Initial trade flows
        self.rewards_log = []  # Store rewards for analysis
        
    def step(self, actions):
        tariffs = np.array(actions) / 10.0  # Normalize tariffs to percentage
        
        trade_impacts = 1 - tariffs  # Higher tariffs reduce trade
        self.trade_flows *= trade_impacts
        
        rewards = self.trade_flows - 0.5 * tariffs  # Countries benefit from trade but suffer from tariffs
        self.rewards_log.append(np.mean(rewards))  # Log average reward
        
        obs = self.trade_flows / np.sum(self.trade_flows)  # Normalize trade balance
        done = False  # Continuous game
        
        return obs, rewards, done, False, {}
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.trade_flows = np.ones(self.num_countries)
        self.rewards_log = []  # Reset log for new episode
        return self.trade_flows / np.sum(self.trade_flows), {}
    
    def render(self):
        print(f"Trade flows: {self.trade_flows}")
    
    def plot_rewards(self):
        plt.plot(self.rewards_log)
        plt.xlabel("Episode Step")
        plt.ylabel("Average Reward")
        plt.title("Reward Progression Over Time")
        plt.show()

# Train PPO agent
env = TariffEnv(num_countries=2)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Evaluate the trained model
done = False
obs, _ = env.reset()
while not done:
    action, _ = model.predict(obs)
    obs, rewards, done, _, _ = env.step(action)
    env.render()

# Plot reward progression
env.plot_rewards()
