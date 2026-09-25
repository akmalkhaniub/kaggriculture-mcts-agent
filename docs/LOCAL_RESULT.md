# Local result

Recorded 2026-09-25 on this machine. This is not a Kaggle leaderboard score. No official simulator spec was available, and no Kaggle API token was provided.

- Entry point: `submission/main.py`
- Policy: UCT MCTS, 40 iterations, rollout depth 4, seed 0
- Environment: local `AgriculturalSimEnv`, deterministic weather, seed 0
- Episode revenue: **272**

Reproduce:

```bash
python submission/main.py
```
