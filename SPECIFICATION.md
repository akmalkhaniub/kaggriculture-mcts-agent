# Technical Specification: Hierarchical MCTS Agricultural Agent
**Project Name:** Hierarchical MCTS Agricultural Agent (Kaggriculture Simulation)  
**Status:** Ready for Implementation  
**Version:** 1.0.0  

---

## 1. System Architecture
The agent architecture separates macro-economic resource forecasting from micro-turn action selection using a hybrid Monte Carlo Tree Search (MCTS) backed by a deep value-policy network.

```mermaid
graph TD
    A[Environment Turn Observation: Weather, Prices, Soil, Competitor Moves] --> B[State Feature Extractor & Feature Normalization]
    B --> C[Value-Policy Network (PyTorch / ONNX)]
    C --> D[Action Prior Probabilities P(s, a)]
    C --> E[State Value Estimation V(s)]
    D --> F[Monte Carlo Tree Search (MCTS) Engine]
    E --> F
    F -->|Rollout Simulations with Fast Transition Model| F
    F --> G[Select Best Action Vector: Plant, Irrigate, Harvest, Trade]
    G --> H[Environment Action Return: < 500ms timeout]
```

---

## 2. Mathematical Formulation & Action Space

### 2.1 Observation State Vector ($S_t$)
- Grid Tensor: Dimensions `(H, W, Channels)` representing soil moisture, nitrogen/phosphorus/potassium levels, crop maturity stage, and pest damage.
- Global Economic Vector: Market commodity prices, interest rates, weather forecasts for the next 5 rounds.
- Opponent State: Resource stockpiles, market positions, and neighboring land boundaries.

### 2.2 Action Space ($A_t$)
Per tile action vector:
1. `NOOP`
2. `TILL_SOIL`
3. `PLANT_CROP(crop_type)`
4. `IRRIGATE(water_volume)`
5. `FERTILIZE(fertilizer_type)`
6. `HARVEST`
7. `MARKET_SELL(quantity, limit_price)`

### 2.3 MCTS Selection Rule (PUCT)
$$a_t = \arg\max_a \left( Q(s, a) + c_{\text{puct}} P(s, a) \frac{\sqrt{\sum_b N(s, b)}}{1 + N(s, a)} \right)$$

---

## 3. Constraints & Submission Format
- **Step Time Limit:** Agent must return action in `< 1000ms` per step.
- **Memory Limit:** Total process RAM `< 2GB`.
- **Packaging:** All neural net weights and logic must compile or pack into a self-contained submission file (e.g. `main.py` with embedded base64 weights or ONNX runtime).

---

## 4. Acceptance Criteria
1. Agent plays complete 200-turn simulation games without timeouts or illegal action exceptions.
2. Achieves > 80% win rate against standard greedy rule-based benchmark bots.
3. Successfully handles severe weather anomalies (drought/floods) through adaptive reservoir management.
