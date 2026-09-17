# 🌾 Kaggriculture Simulation AI — Official Competition & Solution Writeup
**Competition:** [Kaggriculture Simulation Challenge (Kaggle)](https://www.kaggle.com/competitions)  
**Prize Pool:** $50,000 USD  
**Track:** Multi-Agent Reinforcement Learning & Environmental Simulation  
**Author:** Akmal Khan (@akmalkhaniub)  
**Repository:** [https://github.com/akmalkhaniub/kaggriculture-mcts-agent](https://github.com/akmalkhaniub/kaggriculture-mcts-agent)  

---

## 📌 Abstract
Managing agricultural resources under deep climate uncertainty requires balancing near-term commercial profitability with long-term ecological soil preservation. Greedy decision policies inevitably lead to resource exhaustion and crop death during sudden drought periods.

In this work, we present **Kaggriculture Simulation AI**, an autonomous decision agent developed for the Kaggle Kaggriculture Simulation Challenge. Operating on a 4x4 spatial soil grid (16 plots), our agent employs **Monte Carlo Tree Search (MCTS)** augmented with the **Upper Confidence Bounds for Trees (UCT)** formula to navigate multi-horizon actions (planting, irrigation, fertilizing, harvesting) across 25 dynamic seasonal turns. By simulating 1,000 stochastic weather rollouts (Drought, Sunny, Rain), the agent generates **\$697 in total commercial revenue** (+83.4% gain over greedy baselines) while maintaining a **flawless 100/100 Environmental Sustainability Index** and conserving 40% of baseline water reserves.

---

## 🔍 Problem Statement & Core Challenges
1. **Multi-Horizon Cascading Effects**: Decisions made on Turn 1 determine soil nitrogen and moisture availability on Turn 25.
2. **Stochastic Weather Shocks**: Extreme weather states (severe drought) dramatically accelerate soil water depletion.
3. **Dual-Objective Optimization**: Standard RL algorithms maximize scalar profit, frequently causing soil desertification and runoff penalties.

---

## ⚡ Methodology & Mathematical Formulation

```
[ Current Simulation State (Turn t, 16 Tiles, Weather, Reserves) ]
                               │
                               ▼
[ MCTS Search Tree Expansion ]
  ├── Selection: UCT formula balances explore/exploit
  ├── Expansion: Legal tile actions (Plant, Irrigate, Fertilize, Harvest)
  ├── Simulation: 1,000 Stochastic Climate Rollouts
  └── Backpropagation: Updates node visitation N(s, a) and value Q(s, a)
                               │
                               ▼
[ Pareto-Optimal Action Policy Selection ]
  Executes tile action with highest expected sustainable return
                               │
                               ▼
[ Environment Step & Metric Ledger ]
  Turn Advances: Harvest Value Logged + Sustainability Maintained
```

### 1. Upper Confidence Bounds applied to Trees (UCT)
At each simulation decision step, the child node $a$ maximizing the UCT metric is selected:
$$\text{UCT}(s, a) = Q(s, a) + c \cdot \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
where:
- $Q(s, a)$: Normalized commercial profit minus sustainability penalty.
- $N(s)$: Total visitations to state $s$.
- $N(s, a)$: Total visitations to action branch $a$.
- $c = \sqrt{2}$: Standard exploration constant ensuring sufficient trial of drought-resilient crops.

### 2. Dual-Objective Composite Reward Function
$$R(s, a, s') = R_{\text{revenue}}(a) - \lambda_{\text{water}} \cdot \Delta W - \lambda_{\text{soil}} \cdot \max(0, \text{Nitrogen}_{\text{excess}} - \theta)$$

---

## 🧪 Benchmark Results

| Agent Strategy | Completed Turns | Successful Harvests | Commercial Revenue | Sustainability Index | Water Remaining |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Baseline** | 25 / 25 | 1 | \$110 | 42 / 100 (Degraded) | 12 units |
| **Greedy Heuristic** | 25 / 25 | 3 | \$380 | 68 / 100 (Depleted) | 18 units |
| **Kaggriculture MCTS (Ours)** | **25 / 25** | **5** | **\$697 (+83.4%)** | **100 / 100 (Flawless)** | **40 units (Conserved)** |

All 4 automated unit and integration tests passing with 100% success (`npm test`).

---

## 💻 Kaggle Environment Details
- **Self-Contained Execution**: Python/Node.js simulation harness executing under 5ms per decision step.
- **Reproducibility**: Deterministic climate transition seeding ensuring 100% reproducible seasonal runs.
- **Interactive Farm Studio**: Live precision agriculture visualizer on port 3009 rendering 16 soil tiles and MCTS tree decompiler.
