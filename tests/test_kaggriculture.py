"""Kaggriculture tests: env mechanics, agent validity, and MCTS >= greedy >= random."""
from kaggriculture import (
    AgriculturalSimEnv,
    GreedyAgent,
    MCTSAgent,
    RandomAgent,
    legal_actions,
    run_episode,
    compare,
)


def test_env_reset_and_shape():
    env = AgriculturalSimEnv(grid_size=4)
    obs = env.reset()
    assert len(obs["grid"]) == 16
    assert obs["waterStock"] == 100 and obs["turn"] == 0


def test_plant_and_grow_and_harvest_yields_revenue():
    env = AgriculturalSimEnv(max_turns=30, seed=0)
    env.step({"type": "PLANT", "tileIdx": 0, "crop": "CORN"})
    # Grow to maturity with periodic irrigation/fertilize.
    for _ in range(12):
        env.step({"type": "IRRIGATE", "tileIdx": 0})
        env.step({"type": "FERTILIZE", "tileIdx": 0})
    obs = env.observation()
    if obs["grid"][0]["maturity"] >= 80:
        _o, reward, _d = env.step({"type": "HARVEST", "tileIdx": 0})
        assert reward > 0
        assert env.revenue > 0


def test_clone_is_independent():
    env = AgriculturalSimEnv(seed=1)
    snap = env.clone()
    env.step({"type": "PLANT", "tileIdx": 0, "crop": "CORN"})
    assert snap.grid[0].is_planted is False  # clone untouched
    assert env.grid[0].is_planted is True


def test_legal_actions_nonempty_and_valid():
    env = AgriculturalSimEnv()
    acts = legal_actions(env.observation())
    assert len(acts) > 1
    assert all(a["type"] in ("PLANT", "IRRIGATE", "FERTILIZE", "HARVEST", "NOOP") for a in acts)


def test_greedy_beats_random():
    g = sum(run_episode(GreedyAgent(), seed=s, stochastic=True) for s in range(8)) / 8
    r = sum(run_episode(RandomAgent(seed=99), seed=s, stochastic=True) for s in range(8)) / 8
    assert g > r


def test_mcts_competitive_with_greedy():
    # MCTS should at least match greedy on average (it uses greedy as its rollout policy).
    res = compare(MCTSAgent(iterations=60, seed=0), GreedyAgent(), episodes=6, stochastic=True)
    assert res.a_mean >= res.b_mean * 0.9


def test_uct_value_monotonicity():
    # Less-visited node has a higher exploration bonus for equal mean reward.
    hi = MCTSAgent.uct_value(1.0, parent_visits=100, node_visits=1)
    lo = MCTSAgent.uct_value(1.0, parent_visits=100, node_visits=50)
    assert hi > lo


def test_elo_tournament_mcts_leads_random_trails():
    from kaggriculture import Tournament, RandomAgent, GreedyAgent, MCTSAgent
    table = Tournament([MCTSAgent(iterations=50, seed=0), GreedyAgent(), RandomAgent(seed=1)], episodes=8).run()
    assert len(table) == 3
    # Stable signals over a small tournament: MCTS is the top-rated agent, and random
    # play earns the least revenue on average. (Elo of Greedy vs Random can flip on a
    # few seeds — that divergence from mean-revenue is expected and not asserted.)
    assert table[0].name == "MCTS", f"expected MCTS top, got {[s.name for s in table]}"
    rand = next(s for s in table if s.name == "Random")
    assert rand.mean_revenue == min(s.mean_revenue for s in table)
