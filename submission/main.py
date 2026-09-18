"""Kaggriculture Kaggle agent entry point.

The competition harness calls agent(observation, configuration) each turn with the
current observation and expects an action dict back. We use the fast, robust greedy
policy here (deterministic, no external deps). The MCTS planner in the package is used
for offline self-play/tuning where a clonable forward model is available.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kaggriculture.agents import GreedyAgent  # noqa: E402

_AGENT = GreedyAgent()


def agent(observation, configuration=None):
    # `observation` is expected to expose the same shape as env.observation().
    obs = observation if isinstance(observation, dict) else getattr(observation, "__dict__", {})
    return _AGENT.act(obs)


if __name__ == "__main__":
    from kaggriculture import AgriculturalSimEnv

    env = AgriculturalSimEnv(seed=0)
    obs, done = env.observation(), False
    while not done:
        obs, _r, done = env.step(agent(obs))
    print(f"Demo episode revenue: {env.revenue}")
