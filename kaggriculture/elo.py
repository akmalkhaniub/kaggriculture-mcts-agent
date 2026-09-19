"""Round-robin tournament with Elo ratings — a measurable agent-strength ranking.

Each agent plays every other over N shared seeds; per-seed higher revenue = a win.
Elo is updated per pairwise match outcome so the leaderboard reflects head-to-head
strength, not just mean score.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .tournament import run_episode


@dataclass
class Standing:
    name: str
    elo: float = 1000.0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    mean_revenue: float = 0.0


def _expected(a: float, b: float) -> float:
    return 1.0 / (1.0 + 10 ** ((b - a) / 400.0))


@dataclass
class Tournament:
    agents: list  # objects with .name and .act
    episodes: int = 12
    k: int = 24
    standings: dict[str, Standing] = field(default_factory=dict)

    def run(self) -> list[Standing]:
        for agent in self.agents:
            self.standings[agent.name] = Standing(name=agent.name)

        # Cache per-agent scores per seed so pairwise comparisons are consistent.
        scores: dict[str, list[int]] = {}
        for agent in self.agents:
            scores[agent.name] = [run_episode(agent, seed=s, stochastic=True) for s in range(self.episodes)]
            self.standings[agent.name].mean_revenue = round(sum(scores[agent.name]) / self.episodes, 1)

        for i in range(len(self.agents)):
            for j in range(i + 1, len(self.agents)):
                a, b = self.agents[i], self.agents[j]
                sa, sb = self.standings[a.name], self.standings[b.name]
                for s in range(self.episodes):
                    ra, rb = scores[a.name][s], scores[b.name][s]
                    if ra > rb:
                        outcome, wa, wb = 1.0, 'a', 'b'
                        sa.wins += 1; sb.losses += 1
                    elif rb > ra:
                        outcome, wa, wb = 0.0, 'b', 'a'
                        sb.wins += 1; sa.losses += 1
                    else:
                        outcome = 0.5
                        sa.draws += 1; sb.draws += 1
                    ea = _expected(sa.elo, sb.elo)
                    sa.elo += self.k * (outcome - ea)
                    sb.elo += self.k * ((1 - outcome) - (1 - ea))

        return sorted(self.standings.values(), key=lambda s: s.elo, reverse=True)


if __name__ == "__main__":  # pragma: no cover
    from .agents import RandomAgent, GreedyAgent, MCTSAgent

    table = Tournament([MCTSAgent(iterations=60, seed=0), GreedyAgent(), RandomAgent(seed=1)], episodes=10).run()
    print(f"{'agent':10s} {'elo':>6s} {'W-L-D':>10s} {'mean$':>8s}")
    for s in table:
        print(f"{s.name:10s} {s.elo:6.0f} {f'{s.wins}-{s.losses}-{s.draws}':>10s} {s.mean_revenue:8.1f}")
