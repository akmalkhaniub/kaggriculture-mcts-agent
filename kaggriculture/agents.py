"""Agents for Kaggriculture: Random baseline, ported Greedy heuristic, and real MCTS."""
from __future__ import annotations

import math
import random
from typing import Protocol

from .env import AgriculturalSimEnv


class Agent(Protocol):
    name: str
    def act(self, obs: dict) -> dict: ...


def legal_actions(obs: dict) -> list[dict]:
    """Enumerate a compact, sensible action set for the current observation."""
    actions: list[dict] = [{"type": "NOOP", "tileIdx": 0}]
    grid = obs["grid"]
    for i, tile in enumerate(grid):
        if tile["isPlanted"]:
            if tile["maturity"] >= 80:
                actions.append({"type": "HARVEST", "tileIdx": i})
            if tile["moisture"] < 60 and obs["waterStock"] >= 10:
                actions.append({"type": "IRRIGATE", "tileIdx": i})
            if tile["nutrients"] < 60 and obs["fertilizerStock"] >= 10:
                actions.append({"type": "FERTILIZE", "tileIdx": i})
        else:
            for crop in ("CORN", "SOYBEANS", "WHEAT"):
                actions.append({"type": "PLANT", "tileIdx": i, "crop": crop})
    return actions


class RandomAgent:
    name = "Random"

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def act(self, obs: dict) -> dict:
        return self._rng.choice(legal_actions(obs))


class GreedyAgent:
    """The ported rule-based heuristic (harvest → irrigate → fertilize → plant)."""

    name = "Greedy"

    def act(self, obs: dict) -> dict:
        grid = obs["grid"]
        for i, t in enumerate(grid):
            if t["isPlanted"] and t["maturity"] >= 80:
                return {"type": "HARVEST", "tileIdx": i}
        if obs["currentWeather"] != "RAINY" and obs["waterStock"] >= 10:
            for i, t in enumerate(grid):
                if t["isPlanted"] and t["moisture"] < 30:
                    return {"type": "IRRIGATE", "tileIdx": i}
        if obs["fertilizerStock"] >= 10:
            for i, t in enumerate(grid):
                if t["isPlanted"] and t["nutrients"] < 30:
                    return {"type": "FERTILIZE", "tileIdx": i}
        if obs["waterStock"] >= 20 and obs["fertilizerStock"] >= 15:
            for i, t in enumerate(grid):
                if not t["isPlanted"]:
                    crop = "SOYBEANS" if t["nutrients"] < 40 else "CORN"
                    return {"type": "PLANT", "tileIdx": i, "crop": crop}
        for i, t in enumerate(grid):
            if t["isPlanted"] and obs["waterStock"] >= 10:
                return {"type": "IRRIGATE", "tileIdx": i}
        return {"type": "NOOP", "tileIdx": 0}


class _Node:
    __slots__ = ("visits", "value", "children", "untried", "action")

    def __init__(self, untried: list[dict], action: dict | None = None) -> None:
        self.visits = 0
        self.value = 0.0
        self.children: list[_Node] = []
        self.untried = untried
        self.action = action


class MCTSAgent:
    """Upper-Confidence-bound-for-Trees planner using env.clone() as a forward model.

    Each act() call runs `iterations` playouts from the current state and returns the
    root child with the highest average return. A greedy default policy guides rollouts.
    """

    name = "MCTS"

    def __init__(self, iterations: int = 120, rollout_depth: int = 6, c: float = 1.414, seed: int | None = None) -> None:
        self.iterations = iterations
        self.rollout_depth = rollout_depth
        self.c = c
        self._rng = random.Random(seed)
        self._greedy = GreedyAgent()

    def act(self, obs: dict, env: AgriculturalSimEnv | None = None) -> dict:
        if env is None:
            # Without a simulate-able env we fall back to the greedy policy.
            return self._greedy.act(obs)

        root = _Node(untried=legal_actions(obs))
        for _ in range(self.iterations):
            sim = env.clone()
            node = root
            ob = obs
            # 1. Selection + expansion
            path = [node]
            done = False
            while not node.untried and node.children and not done:
                node = self._uct_select(node)
                ob, r, done = sim.step(node.action)
                path.append(node)
            if node.untried and not done:
                action = node.untried.pop(self._rng.randrange(len(node.untried)))
                ob, r, done = sim.step(action)
                child = _Node(untried=legal_actions(ob), action=action)
                node.children.append(child)
                path.append(child)
            # 2. Rollout (greedy default policy)
            total = self._rollout(sim, ob, done)
            # 3. Backprop
            for n in path:
                n.visits += 1
                n.value += total

        if not root.children:
            return self._greedy.act(obs)
        best = max(root.children, key=lambda n: n.value / n.visits if n.visits else -1e9)
        return best.action

    def _uct_select(self, node: _Node) -> _Node:
        logN = math.log(node.visits + 1)
        return max(
            node.children,
            key=lambda ch: (ch.value / ch.visits if ch.visits else 1e9) + self.c * math.sqrt(logN / (ch.visits + 1e-9)),
        )

    def _rollout(self, sim: AgriculturalSimEnv, ob: dict, done: bool) -> float:
        total = 0.0
        depth = 0
        while not done and depth < self.rollout_depth:
            action = self._greedy.act(ob)
            ob, r, done = sim.step(action)
            total += r
            depth += 1
        return total

    @staticmethod
    def uct_value(mean_reward: float, parent_visits: int, node_visits: int, c: float = 1.414) -> float:
        if node_visits == 0:
            return math.inf
        return mean_reward + c * math.sqrt(math.log(parent_visits) / node_visits)
