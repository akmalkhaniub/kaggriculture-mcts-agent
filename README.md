# 🌾 Kaggriculture MCTS Agent — Climate-Resilient Agricultural Digital Twin

[![Kaggle Simulations](https://img.shields.io/badge/Kaggle-Simulations_Competition_2026-20beff.svg)](https://www.kaggle.com/competitions)
[![Environment](https://img.shields.io/badge/Gymnasium-Digital_Twin_2026-green.svg)](https://gymnasium.farama.org/)
[![Algorithm](https://img.shields.io/badge/Algorithm-Monte_Carlo_Tree_Search_(MCTS)-blue.svg)](#mcts-agent--uct-decision-engine)
[![Sustainability](https://img.shields.io/badge/Sustainability_Score-100%2F100-brightgreen.svg)](#end-of-season-sustainability-metrics)
[![Crop Dynamics](https://img.shields.io/badge/Agronomics-Nitrogen_Fixation_%26_Rotation-amber.svg)](#soil--crop-rotation-dynamics)
[![Tests Passing](https://img.shields.io/badge/Tests-4%2F4_Passed_100%25-brightgreen.svg)](#test-verification)

> **Autonomous agronomic decision-making agent for the Kaggle Simulations Agricultural Challenge.** Employs **Monte Carlo Tree Search (MCTS)** with Upper Confidence Bound applied to Trees (UCT) inside a stochastic **Gymnasium digital twin**, optimizing commercial crop yield while maintaining a **100/100 Environmental Sustainability Index**.

---

## 📌 Executive Summary & Hackathon Pitch

Agricultural producers face compounding crises: increasing climate volatility (prolonged droughts and unpredictable deluge events), volatile fertilizer prices, and rapid soil nutrient depletion from monocropping.
- Pure greedy heuristics over-fertilize and exhaust water tables, collapsing farm viability in later seasons.
- Standard Reinforcement Learning (e.g. PPO/DQN) struggles with delayed sparse rewards and abrupt climate distribution shifts.

### The Kaggriculture MCTS Solution
1. **High-Fidelity Agronomic Digital Twin**: Models 16 discrete plots ($4 \times 4$), dynamic soil nitrogen budgets, soil moisture evapotranspiration, and pathogen accumulation.
2. **Crop Rotation & Symbiosis**: Rewards alternating nitrogen-fixing legumes (Soybeans) with nitrogen-consuming cereals (Corn, Wheat) to restore soil fertility naturally without chemical runoff.
3. **Stochastic Weather Markov Chain**: Simulates sunny days, beneficial rain, and crippling droughts.
4. **MCTS with UCT Exploration**: Explores deep decision branches into future seasons using the UCT formula:
   $$\text{UCT} = Q(s, a) + c \cdot \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
   guaranteeing optimal trade-offs between immediate harvest revenues and long-term soil health.

---

## 🏛️ System Architecture

```
  +-----------------------------------------------------------------------------------------+
  |                           AGRONOMIC DIGITAL TWIN ENVIRONMENT                            |
  |                                                                                         |
  |   +--------------------------+    +---------------------------+    +----------------+   |
  |   | 16-Plot Soil Grid (4x4)  |    | Dynamic Nitrogen/Moisture |    | Weather Markov |   |
  |   | Wheat / Corn / Soy / Rice|    | Evapotranspiration Decay  |    | Sun / Rain /   |   |
  |   +--------------------------+    +---------------------------+    | Drought        |   |
  |                                                                    +----------------+   |
  +--------------------------------------------+--------------------------------------------+
                                               |
                                               v State Vector S_t
  +-----------------------------------------------------------------------------------------+
  |                      MONTE CARLO TREE SEARCH (MCTS) DECISION ENGINE                     |
  |                                                                                         |
  |   1. SELECTION                   2. EXPANSION                 3. SIMULATION (ROLLOUT)   |
  |   Traverse existing tree         Add valid actions to leaf:   Fast forward K turns with |
  |   via UCT formula:               • PLANT (Crop Type)          stochastic weather shocks |
  |   Argmax [ Q + c * sqrt(ln/n) ]  • IRRIGATE / FERTILIZE       to terminal season        |
  |                                  • HARVEST / FALLOW                                     |
  |                                                                                         |
  |                                         4. BACKPROPAGATION                              |
  |                                         Propagate Reward = Revenue + Sustainability     |
  |                                         up all ancestor nodes in tree                   |
  +--------------------------------------------+--------------------------------------------+
                                               |
                                               v Optimal Action a*
  +-----------------------------------------------------------------------------------------+
  |                                  EXECUTION & HARVEST YIELD                              |
  |                                                                                         |
  |       Revenue Generated: +$697.00  |  Sustainability Score: 100/100 (Zero Depletion)    |
  +-----------------------------------------------------------------------------------------+
```

---

## 🔬 Core Engineering Modules

| Module | Source File | Functionality |
| :--- | :--- | :--- |
| **Agricultural Sim Environment** | [`src/agricultural_sim_env.js`](src/agricultural_sim_env.js) | Gym-style environment implementing soil moisture decay, nitrogen depletion/fixation, crop lifecycle, and Markov weather transitions. |
| **MCTS Agent** | [`src/mcts_agent.js`](src/mcts_agent.js) | Monte Carlo Tree Search planner with UCT action selection, rollouts, and reward backpropagation. |
| **Interactive Farm Simulator** | [`src/server.js`](src/server.js) + [`src/public/index.html`](src/public/index.html) | Interactive web dashboard rendering the 16-plot farm grid, real-time crop growth animations, weather forecasts, and revenue charts. |

---

## ⚡ Quickstart Guide

### 1. Installation
```bash
git clone https://github.com/akmalkhaniub/kaggriculture-mcts-agent.git
cd kaggriculture-mcts-agent
npm install
```

### 2. Run Automated Verification Test Suite
```bash
npm test
```

### 3. Launch Interactive Farm Dashboard
```bash
node src/server.js
```
Open **`http://localhost:3009`** in your browser:
- Watch the MCTS agent autonomously manage 16 crop plots across seasons.
- Observe dynamic crop rotation (Soybean $\rightarrow$ Corn) automatically replenishing soil nitrogen.
- Monitor real-time weather shock adaptations during sudden severe droughts.
- Track harvest revenue growth and sustainable water conservation curves.

---

## 🧪 Test Verification

The test suite validates environmental state transitions and MCTS UCT calculations:

```text
> kaggriculture-mcts-agent@1.0.0 test
> node test/verify_kaggriculture.js

🧪 Starting Kaggriculture Simulation Automated Verification Suite (Kaggle 2026)...

1️⃣ Initializing 4x4 Agricultural Environment...
   ✅ Grid initialized: 16 plots, Water: 100 units, Fertilizer: 50 units, Weather: SUNNY.
2️⃣ Running 25-Turn Competitive Agricultural Simulation...
   🌾 Turn 4: [HARVEST Tile #0] Harvested yield worth +$153! (Weather: DROUGHT)
   🌾 Turn 5: [HARVEST Tile #1] Harvested yield worth +$153! (Weather: SUNNY)
   🌾 Turn 6: [HARVEST Tile #2] Harvested yield worth +$153! (Weather: SUNNY)
   🌾 Turn 14: [HARVEST Tile #0] Harvested yield worth +$119! (Weather: DROUGHT)
   🌾 Turn 20: [HARVEST Tile #1] Harvested yield worth +$119! (Weather: SUNNY)

3️⃣ Evaluating End-of-Season Performance Metrics:
   • Total Completed Turns: 25 / 25
   • Successful Harvest Operations: 5
   • Total Commercial Revenue Generated: $697
   • Environmental Sustainability Index: 100 / 100
   • Remaining Water Reserves: 40 units

4️⃣ Testing MCTS UCT (Upper Confidence Bound) Formula...
   ✅ MCTS UCT Value (Q=140, N_p=100, N_c=10): 140.96

🎉 ALL KAGGRICULTURE SIMULATION TESTS PASSED WITH 100% SUCCESS!
```

---

## 🌾 Agronomic Dynamics & Action Space

- **Actions**:
  - `PLANT(plot_idx, crop_type)`: Seeds Wheat, Soybeans, Corn, or Rice.
  - `IRRIGATE(plot_idx)`: Conserves ground moisture during drought conditions.
  - `FERTILIZE(plot_idx)`: Augments plot nitrogen level.
  - `HARVEST(plot_idx)`: Reaps mature crop yielding commercial revenue.
  - `FALLOW(plot_idx)`: Lets plot rest, restoring baseline microbial health.
- **Reward Function**:
  $$R_t = \text{Revenue}(\text{Harvest}_t) - \text{ResourceCosts} + \lambda_{\text{sustain}} \cdot \text{SoilHealth}$$

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
