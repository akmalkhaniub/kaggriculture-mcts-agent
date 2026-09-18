# Roadmap & Milestones: Hierarchical MCTS Agricultural Agent
**Hackathon:** Kaggriculture Simulation  
**Target:** Kaggle Simulation Competition  

---

> **Status legend (updated 2026-09-18):** `[x]` implemented in code · `[~]` partial / stand-in (working JS prototype, not the production stack named) · `[ ]` not started.
> **Reality note:** **Rebuilt in Python** (`kaggriculture/` package; old Node prototype under `legacy-js/`). Clonable digital-twin env + a ported greedy agent + a **real UCT MCTS** planner (selection/expansion/rollout/backprop via `env.clone()`), a tournament harness, and a Kaggle `submission/main.py` agent entry point. 7 pytest cases pass (greedy beats random; MCTS competitive with greedy). No neural policy-value net yet - a strong simulation baseline, not a leaderboard winner.

## Phase 1: Environment Gym & Heuristic Baseline (Milestone 1)
- [x] Setup standalone local reproduction of the Kaggriculture game rules and gym environment. *(JS sim env)*
- [~] Implement robust greedy heuristic agent (baseline agricultural bot: soil balance + auto-harvest).
- [~] Build automated head-to-head match runner with Elo rating calculation.

## Phase 2: Monte Carlo Tree Search (MCTS) Engine (Milestone 2)
- [~] Implement fast simulation forward model in Python/Numba capable of > 10,000 rollouts/sec. *(JS forward model)*
- [x] Build standard UCT/PUCT search tree with state transpositions and pruning.
- [~] Verify that MCTS agent consistently outperforms the greedy baseline bot (> 75% win rate). *(demo scale)*

## Phase 3: Neural Policy-Value Network Training (Milestone 3)
- [ ] Train convolutional policy-value network using self-play trajectories.
- [ ] Integrate neural priors into the MCTS rollout guidance.
- [ ] Optimize inference using ONNX Runtime to guarantee turn execution in < 400ms.

## Phase 4: Bundling & Kaggle Ladder Submission (Milestone 4)
- [ ] Bundle neural weights and MCTS solver into a single submission `main.py`.
- [ ] Validate submission file against Kaggle's local CLI validation environment.
- [ ] Submit to Kaggle leaderboard, observe matchmaking replays, and iterate on adversarial edge cases.
