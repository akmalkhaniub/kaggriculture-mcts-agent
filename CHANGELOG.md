# Changelog

## [Unreleased]

### Rebuilt in Python for Kaggle (2026-09-18)
Rebuilt from the Node prototype (preserved under `legacy-js/`) into a self-contained
Python simulation + agents, the form a Kaggle simulation competition submits.

### Added
- `kaggriculture/env.py` — clonable digital-twin environment (crops, weather, soil,
  sustainability), usable as an exact MCTS forward model.
- `kaggriculture/agents.py` — `RandomAgent`, ported `GreedyAgent`, and a **real UCT
  MCTSAgent** (selection/expansion/greedy rollout/backprop via `env.clone()`).
- `kaggriculture/tournament.py` — episode runner + head-to-head comparison.
- `submission/main.py` — Kaggle `agent(observation, configuration)` entry point.
- `tests/test_kaggriculture.py` — 7 pytest cases (mechanics, clone independence, action
  legality, UCT monotonicity, greedy>random, MCTS competitive with greedy).
- `pyproject.toml`, CI on Python 3.10–3.12.

### Notes
- Submitted policy is the fast greedy agent; MCTS plans ahead but is slower (offline
  self-play/tuning). A neural policy-value net is the next step for leaderboard climbing.
