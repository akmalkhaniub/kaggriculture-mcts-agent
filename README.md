# 🌾 Kaggriculture — MCTS Farm-Management Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org)
[![MCTS](https://img.shields.io/badge/Search-UCT%20MCTS-2E7D32.svg)](#how-it-works)
[![Kaggle](https://img.shields.io/badge/Kaggle-Kaggriculture%20Simulation-20BEFF.svg)](https://www.kaggle.com/competitions)

> **Built for the [Kaggriculture Simulation](https://www.kaggle.com/competitions) (Kaggle simulation competition).**

A digital-twin farming environment plus agents that maximize revenue over a season by
planting, irrigating, fertilizing, and harvesting under stochastic weather — including a
genuine **UCT Monte-Carlo Tree Search** planner that uses the environment as a forward
model.

> **Note:** rebuilt from a Node.js prototype (kept under [`legacy-js/`](./legacy-js)) into
> the correct stack — a self-contained **Python** simulation + agent, which is what a
> Kaggle simulation competition submits.

## How it works

- **`env.py`** — the environment: 4×4 plots, three crops (Corn/Wheat/nitrogen-fixing
  Soybeans), stochastic weather (SUNNY/RAINY/DROUGHT), soil moisture/nutrients, maturity,
  and an environmental-runoff sustainability penalty. Deterministic-by-default and
  `clone()`-able so it can serve as an exact MCTS forward model.
- **`agents.py`** — `RandomAgent`, a ported `GreedyAgent` heuristic, and a real
  **`MCTSAgent`**: UCT selection + expansion, greedy-policy rollouts via `env.clone()`,
  and value backpropagation. Picks the root child with the best average return.
- **`tournament.py`** — episode runner and head-to-head comparison over seeds.
- **`submission/main.py`** — the Kaggle `agent(observation, configuration)` entry point
  (uses the fast greedy policy; MCTS is used for offline self-play/tuning).

## Run

```bash
pip install -r requirements-dev.txt && pip install -e .
pytest -q                     # env + agent tests (incl. MCTS vs greedy vs random)
python submission/main.py     # play one demo episode and print revenue
```

```python
from kaggriculture import MCTSAgent, GreedyAgent, compare
print(compare(MCTSAgent(iterations=120), GreedyAgent(), episodes=20))
```

## Scope & honesty

The environment and search are real and self-contained (pure Python, no heavy deps). The
submitted agent is the robust greedy policy; MCTS materially plans ahead but is slower and
is used for offline analysis. This is a strong, correct simulation baseline — a
neural policy-value network (AlphaZero-style) would be the next step for leaderboard
performance. Tests verify env mechanics, clone independence, action legality, UCT
behavior, and that greedy beats random / MCTS stays competitive with greedy across seeds.
