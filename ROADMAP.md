# Roadmap & Milestones: Hierarchical MCTS Agricultural Agent
**Hackathon:** Kaggriculture Simulation  
**Target:** Kaggle Simulation Competition  

---

## Phase 1: Environment Gym & Heuristic Baseline (Milestone 1)
- [ ] Setup standalone local reproduction of the Kaggriculture game rules and gym environment.
- [ ] Implement robust greedy heuristic agent (baseline agricultural bot: soil balance + auto-harvest).
- [ ] Build automated head-to-head match runner with Elo rating calculation.

## Phase 2: Monte Carlo Tree Search (MCTS) Engine (Milestone 2)
- [ ] Implement fast simulation forward model in Python/Numba capable of > 10,000 rollouts/sec.
- [ ] Build standard UCT/PUCT search tree with state transpositions and pruning.
- [ ] Verify that MCTS agent consistently outperforms the greedy baseline bot (> 75% win rate).

## Phase 3: Neural Policy-Value Network Training (Milestone 3)
- [ ] Train convolutional policy-value network using self-play trajectories.
- [ ] Integrate neural priors into the MCTS rollout guidance.
- [ ] Optimize inference using ONNX Runtime to guarantee turn execution in < 400ms.

## Phase 4: Bundling & Kaggle Ladder Submission (Milestone 4)
- [ ] Bundle neural weights and MCTS solver into a single submission `main.py`.
- [ ] Validate submission file against Kaggle's local CLI validation environment.
- [ ] Submit to Kaggle leaderboard, observe matchmaking replays, and iterate on adversarial edge cases.
