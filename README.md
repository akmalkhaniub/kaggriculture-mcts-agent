# Kaggriculture Simulation Competition

- **Official Challenge URL:** [https://www.kaggle.com/competitions](https://www.kaggle.com/competitions)
- **Organizer:** Kaggle
- **Host Platform:** Kaggle Competitions
- **Total Prize Pool:** $50,000 USD
- **Format:** Simulation Competition (Bot vs Bot / Leaderboard Matchmaking)
- **Primary Themes:** Multi-Agent Reinforcement Learning (MARL), Game Theory, Strategic Simulation, Resource Optimization

---

## 1. Challenge Overview & Problem Statement
Kaggriculture is a competitive multi-agent simulation game where multiple algorithmic agents compete and cooperate within a shared agricultural grid world.

Agents must manage resources (water, soil nutrients, seeds, labor), react to dynamic environmental fluctuations (droughts, market price volatility, pest invasions), and optimize agricultural yield while interacting with rival agents on neighboring plots.

### Evaluation Rules
- Agents submit a self-contained Python script implementing an `agent(observation, configuration) -> action` interface.
- Bots compete in round-robin tournament matches on Kaggle's rating ladder (TrueSkill / Elo system).

---

## 2. Selected Architectural Strategy: Hierarchical Reinforcement Learning & Monte Carlo Tree Search (HRL-MCTS)
1. **High-Level Strategic Planner:** Evaluates long-horizon macro strategies (crop diversification vs monoculture cash-crops, cooperative trading vs competitive hoarding).
2. **Low-Level Tactical Policy:** Fast neural policy (PPO/A2C) or rule-based heuristic controller that executes turn-by-turn micro-actions (irrigate, plant, fertilize, harvest, trade).
3. **Rollout Simulator & Fast Forward Search:** In-memory C++/Numba forward simulation engine to predict opponent moves 3-5 turns ahead and prevent catastrophic crop loss.

---

## 3. Directory Structure
```
kaggle-kaggriculture/
├── README.md               # Challenge rules, environment API, rating system (this file)
├── SPECIFICATION.md        # Environment state space, action vectors, MCTS algorithm
├── ROADMAP.md              # Self-play training and submission milestones
├── sim/                    # Fast simulation environment & state transition logic
├── agents/                 # Heuristic baseline, PPO policy & MCTS search agent
├── training/               # Self-play reinforcement learning harness (Ray / RLlib)
└── submission/             # Bundled single-file Kaggle submission bot
```
