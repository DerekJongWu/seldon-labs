import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, namedtuple
import random
from typing import List, Dict, Tuple
import gym
from gym import spaces

Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])

class PolicyEnvironment(gym.Env):
    """Custom environment for policy simulation"""
    def __init__(self, num_agents: int, state_size: int, action_size: int):
        super().__init__()
        
        self.num_agents = num_agents
        self.state_size = state_size
        self.action_size = action_size
        
        # Define action and observation spaces
        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(action_size,), dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(state_size,), dtype=np.float32
        )
        
        # Initial state variables
        self.reset()
    
    def reset(self):
        """Reset environment to initial state"""
        self.current_step = 0
        self.states = np.random.normal(0, 1, (self.num_agents, self.state_size))
        return self.states
    
    def step(self, actions: np.ndarray) -> Tuple[np.ndarray, np.ndarray, bool, dict]:
        """Execute one timestep of the environment"""
        self.current_step += 1
        
        # Calculate rewards based on actions and current state
        rewards = self._calculate_rewards(actions)
        
        # Update states based on actions
        self._update_states(actions)
        
        # Check if episode is done
        done = self.current_step >= 100  # Example episode length
        
        return self.states, rewards, done, {}
    
    def _calculate_rewards(self, actions: np.ndarray) -> np.ndarray:
        """Calculate rewards for each agent based on their actions and states"""
        rewards = np.zeros(self.num_agents)
        
        for i in range(self.num_agents):
            # Example reward function considering both individual and collective outcomes
            individual_utility = np.sum(actions[i] * self.states[i])
            social_welfare = -0.1 * np.sum(np.abs(actions[i]))  # Penalty for extreme actions
            
            # Competition effects
            for j in range(self.num_agents):
                if i != j:
                    # Agents can be affected by others' actions
                    interaction = -0.05 * np.sum(np.abs(actions[i] - actions[j]))
                    social_welfare += interaction
            
            rewards[i] = individual_utility + social_welfare
            
        return rewards
    
    def _update_states(self, actions: np.ndarray):
        """Update environment states based on actions"""
        # State transition dynamics
        state_change = 0.1 * actions + 0.01 * np.random.normal(0, 1, self.states.shape)
        self.states += state_change
        
        # Add some constraints to keep states bounded
        self.states = np.clip(self.states, -5, 5)

class DQNAgent:
    """Deep Q-Network agent"""
    def __init__(self, state_size: int, action_size: int, hidden_size: int = 128):
        self.state_size = state_size
        self.action_size = action_size
        
        # Neural network for Q-function approximation
        self.network = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size)
        )
        
        self.optimizer = optim.Adam(self.network.parameters(), lr=0.001)
        self.memory = deque(maxlen=10000)
        self.batch_size = 64
        self.gamma = 0.99  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
    def act(self, state: np.ndarray) -> np.ndarray:
        """Select action based on epsilon-greedy policy"""
        if random.random() < self.epsilon:
            return np.random.uniform(-1, 1, self.action_size)
        
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.network(state_tensor)
        return q_values.numpy()[0]
    
    def remember(self, experience: Experience):
        """Store experience in replay memory"""
        self.memory.append(experience)
    
    def learn(self):
        """Update policy based on experiences in memory"""
        if len(self.memory) < self.batch_size:
            return
        
        # Sample random batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states = torch.FloatTensor([e.state for e in batch])
        actions = torch.FloatTensor([e.action for e in batch])
        rewards = torch.FloatTensor([e.reward for e in batch])
        next_states = torch.FloatTensor([e.next_state for e in batch])
        dones = torch.FloatTensor([e.done for e in batch])
        
        # Calculate target Q-values
        with torch.no_grad():
            next_q_values = self.network(next_states)
            max_next_q = next_q_values.max(1)[0]
            targets = rewards + self.gamma * max_next_q * (1 - dones)
        
        # Calculate current Q-values
        q_values = self.network(states)
        q_values = torch.sum(q_values * actions, dim=1)
        
        # Update network
        loss = nn.MSELoss()(q_values, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay exploration rate
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

class PolicySimulation:
    """Main simulation class for multi-agent policy learning"""
    def __init__(self, num_agents: int, state_size: int, action_size: int):
        self.env = PolicyEnvironment(num_agents, state_size, action_size)
        self.agents = [DQNAgent(state_size, action_size) for _ in range(num_agents)]
        
        self.state_history = []
        self.reward_history = []
        self.action_history = []
    
    def run_episode(self) -> Tuple[List[float], List[np.ndarray]]:
        """Run one episode of the simulation"""
        states = self.env.reset()
        episode_rewards = []
        done = False
        
        while not done:
            # Get actions from all agents
            actions = np.array([agent.act(states[i]) for i, agent in enumerate(self.agents)])
            
            # Execute actions in environment
            next_states, rewards, done, _ = self.env.step(actions)
            
            # Store experiences and learn
            for i, agent in enumerate(self.agents):
                experience = Experience(
                    states[i], actions[i], rewards[i], next_states[i], done
                )
                agent.remember(experience)
                agent.learn()
            
            states = next_states
            episode_rewards.append(rewards)
            
            # Store history
            self.state_history.append(states.copy())
            self.reward_history.append(rewards.copy())
            self.action_history.append(actions.copy())
        
        return episode_rewards, states

# Example usage
def run_policy_simulation():
    # Initialize simulation parameters
    num_agents = 3
    state_size = 5  # Size of state vector for each agent
    action_size = 3  # Size of action vector for each agent
    num_episodes = 100
    
    # Create simulation
    sim = PolicySimulation(num_agents, state_size, action_size)
    
    # Run episodes
    all_rewards = []
    for episode in range(num_episodes):
        episode_rewards, final_states = sim.run_episode()
        mean_reward = np.mean(episode_rewards)
        all_rewards.append(mean_reward)
        
        if episode % 10 == 0:
            print(f"Episode {episode}, Mean Reward: {mean_reward:.2f}")
    
    return sim, all_rewards

if __name__ == "__main__":
    sim, rewards = run_policy_simulation()
    print("\nSimulation complete!")
    print(f"Final average reward: {np.mean(rewards[-10:]):.2f}")