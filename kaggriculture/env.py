"""Kaggriculture digital-twin environment (single-agent resource management).

Deterministic weather cycle by default (seedable stochastic option), so it can be
used as an exact forward model inside MCTS via :meth:`clone`.
"""
from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field

CROPS = {
    "WHEAT": {"name": "Wheat", "yield": 120, "water_req": 25, "nutrient_req": 20, "fixes_nitrogen": False},
    "CORN": {"name": "Corn", "yield": 180, "water_req": 35, "nutrient_req": 30, "fixes_nitrogen": False},
    "SOYBEANS": {"name": "Soybeans", "yield": 140, "water_req": 20, "nutrient_req": 10, "fixes_nitrogen": True},
}

ACTION_TYPES = ("PLANT", "IRRIGATE", "FERTILIZE", "HARVEST", "NOOP")


@dataclass
class Tile:
    moisture: int = 50
    nutrients: int = 50
    maturity: int = 0
    is_planted: bool = False
    crop_type: str | None = None

    def as_dict(self) -> dict:
        return {
            "moisture": self.moisture,
            "nutrients": self.nutrients,
            "maturity": self.maturity,
            "isPlanted": self.is_planted,
            "cropType": self.crop_type,
        }


@dataclass
class AgriculturalSimEnv:
    grid_size: int = 4
    max_turns: int = 30
    stochastic: bool = False
    seed: int | None = None
    weather_states: tuple[str, ...] = ("SUNNY", "RAINY", "SUNNY", "DROUGHT", "SUNNY")
    current_turn: int = 0
    revenue: int = 0
    water_stock: int = 100
    fertilizer_stock: int = 50
    current_weather: str = "SUNNY"
    environmental_runoff: int = 0
    grid: list[Tile] = field(default_factory=list)
    _rng: random.Random = field(default_factory=random.Random, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self.reset()

    def reset(self) -> dict:
        self.current_turn = 0
        self.revenue = 0
        self.water_stock = 100
        self.fertilizer_stock = 50
        self.current_weather = "SUNNY"
        self.environmental_runoff = 0
        self.grid = [Tile() for _ in range(self.grid_size * self.grid_size)]
        return self.observation()

    def clone(self) -> "AgriculturalSimEnv":
        return copy.deepcopy(self)

    def observation(self) -> dict:
        return {
            "turn": self.current_turn,
            "maxTurns": self.max_turns,
            "waterStock": self.water_stock,
            "fertilizerStock": self.fertilizer_stock,
            "totalRevenue": self.revenue,
            "currentWeather": self.current_weather,
            "environmentalRunoff": self.environmental_runoff,
            "sustainabilityIndex": max(0, 100 - round(self.environmental_runoff * 1.2)),
            "grid": [t.as_dict() for t in self.grid],
        }

    def _next_weather(self) -> str:
        if self.stochastic:
            return self._rng.choices(["SUNNY", "RAINY", "DROUGHT"], weights=[0.55, 0.3, 0.15])[0]
        return self.weather_states[self.current_turn % len(self.weather_states)]

    def step(self, action: dict) -> tuple[dict, int, bool]:
        turn_reward = 0
        idx = action.get("tileIdx", 0)
        atype = action.get("type", "NOOP")
        self.current_weather = self._next_weather()

        if 0 <= idx < len(self.grid):
            tile = self.grid[idx]
            if atype == "PLANT" and not tile.is_planted:
                tile.is_planted = True
                tile.crop_type = action.get("crop", "WHEAT")
                tile.maturity = 10
            elif atype == "IRRIGATE" and self.water_stock >= 10:
                self.water_stock -= 10
                tile.moisture = min(100, tile.moisture + 30)
            elif atype == "FERTILIZE" and self.fertilizer_stock >= 10:
                self.fertilizer_stock -= 10
                tile.nutrients = min(100, tile.nutrients + 30)
                if tile.moisture > 70:
                    self.environmental_runoff += 5
            elif atype == "HARVEST" and tile.is_planted and tile.maturity >= 80:
                crop = CROPS.get(tile.crop_type or "WHEAT", CROPS["WHEAT"])
                gained = round((tile.maturity / 100) * crop["yield"])
                self.revenue += gained
                turn_reward += gained
                if crop["fixes_nitrogen"]:
                    tile.nutrients = min(100, tile.nutrients + 20)
                tile.is_planted = False
                tile.crop_type = None
                tile.maturity = 0

        delta = 20 if self.current_weather == "RAINY" else (-25 if self.current_weather == "DROUGHT" else -15)
        for t in self.grid:
            if t.is_planted:
                if t.moisture >= 25 and t.nutrients >= 25:
                    t.maturity = min(100, t.maturity + 25)
                t.moisture = max(0, min(100, t.moisture + delta))
                t.nutrients = max(0, t.nutrients - 10)
            elif self.current_weather == "RAINY":
                t.moisture = min(100, t.moisture + 15)

        self.current_turn += 1
        done = self.current_turn >= self.max_turns
        return self.observation(), turn_reward, done
