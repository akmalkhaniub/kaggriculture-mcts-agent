"""Kaggriculture — digital-twin farm simulation with Greedy and MCTS agents."""
from .env import AgriculturalSimEnv, CROPS, ACTION_TYPES
from .agents import Agent, RandomAgent, GreedyAgent, MCTSAgent, legal_actions
from .tournament import run_episode, compare, MatchResult

__all__ = [
    "AgriculturalSimEnv", "CROPS", "ACTION_TYPES",
    "Agent", "RandomAgent", "GreedyAgent", "MCTSAgent", "legal_actions",
    "run_episode", "compare", "MatchResult",
]
__version__ = "1.0.0"
