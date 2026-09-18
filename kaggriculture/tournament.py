"""Episode runner + head-to-head comparison for Kaggriculture agents."""
from __future__ import annotations

from dataclasses import dataclass

from .agents import MCTSAgent
from .env import AgriculturalSimEnv


def run_episode(agent, seed: int | None = None, stochastic: bool = False, max_turns: int = 30) -> int:
    """Run one episode and return the final revenue. MCTS gets the live env as a model."""
    env = AgriculturalSimEnv(max_turns=max_turns, stochastic=stochastic, seed=seed)
    obs = env.observation()
    done = False
    while not done:
        if isinstance(agent, MCTSAgent):
            action = agent.act(obs, env=env)
        else:
            action = agent.act(obs)
        obs, _r, done = env.step(action)
    return env.revenue


@dataclass
class MatchResult:
    agent_a: str
    agent_b: str
    a_mean: float
    b_mean: float
    a_wins: int
    b_wins: int
    episodes: int

    @property
    def a_win_rate(self) -> float:
        return self.a_wins / self.episodes if self.episodes else 0.0


def compare(agent_a, agent_b, episodes: int = 20, stochastic: bool = True) -> MatchResult:
    a_scores, b_scores = [], []
    a_wins = b_wins = 0
    for s in range(episodes):
        sa = run_episode(agent_a, seed=s, stochastic=stochastic)
        sb = run_episode(agent_b, seed=s, stochastic=stochastic)
        a_scores.append(sa)
        b_scores.append(sb)
        if sa >= sb:
            a_wins += 1
        else:
            b_wins += 1
    return MatchResult(
        agent_a=getattr(agent_a, "name", "A"),
        agent_b=getattr(agent_b, "name", "B"),
        a_mean=sum(a_scores) / episodes,
        b_mean=sum(b_scores) / episodes,
        a_wins=a_wins,
        b_wins=b_wins,
        episodes=episodes,
    )
