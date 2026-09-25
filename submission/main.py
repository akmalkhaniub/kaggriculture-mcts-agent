"""Kaggriculture agent entry point.

The harness calls agent(observation, configuration) each turn. MCTS needs a
forward model, so the observation is rebuilt into the local simulator. No
official competition environment was available in this repo; if the harness
observation shape differs, the agent falls back to greedy.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kaggriculture.agents import GreedyAgent, MCTSAgent  # noqa: E402
from kaggriculture.env import AgriculturalSimEnv  # noqa: E402

# Time-capped search: small iteration budget so a turn stays interactive.
_MCTS = MCTSAgent(iterations=40, rollout_depth=4, seed=0)
_GREEDY = GreedyAgent()


def agent(observation, configuration=None):
    obs = observation if isinstance(observation, dict) else getattr(observation, "__dict__", {})
    try:
        env = AgriculturalSimEnv.from_observation(obs)
        return _MCTS.act(obs, env)
    except Exception:
        return _GREEDY.act(obs)


if __name__ == "__main__":
    env = AgriculturalSimEnv(seed=0)
    obs, done = env.observation(), False
    while not done:
        obs, _r, done = env.step(agent(obs))
    print(f"Demo episode revenue: {env.revenue}")
