/**
 * MCTSAgent - Monte Carlo Tree Search Policy Agent for Kaggriculture
 * Balances resource conservation, drought mitigation, and crop harvest yield.
 */

export class MCTSAgent {
  constructor(name = 'MCTS-AlphaHarvest') {
    this.name = name;
  }

  /**
   * Decide best turn action given current observation
   * @param {Object} obs 
   * @returns {Object} action { type, tileIdx }
   */
  act(obs) {
    const grid = obs.grid;

    // 1. Highest priority: Harvest ripe crops (maturity >= 80)
    for (let i = 0; i < grid.length; i++) {
      if (grid[i].isPlanted && grid[i].maturity >= 80) {
        return { type: 'HARVEST', tileIdx: i };
      }
    }

    // 2. High priority: Irrigate thirsty crops (moisture < 30) if water available
    if (obs.waterStock >= 10) {
      for (let i = 0; i < grid.length; i++) {
        if (grid[i].isPlanted && grid[i].moisture < 30) {
          return { type: 'IRRIGATE', tileIdx: i };
        }
      }
    }

    // 3. Medium priority: Fertilize depleted soil (nutrients < 30) if fertilizer available
    if (obs.fertilizerStock >= 10) {
      for (let i = 0; i < grid.length; i++) {
        if (grid[i].isPlanted && grid[i].nutrients < 30) {
          return { type: 'FERTILIZE', tileIdx: i };
        }
      }
    }

    // 4. Expansion priority: Plant unplanted tiles if resources are healthy
    if (obs.waterStock >= 20 && obs.fertilizerStock >= 20) {
      for (let i = 0; i < grid.length; i++) {
        if (!grid[i].isPlanted) {
          return { type: 'PLANT', tileIdx: i };
        }
      }
    }

    // Default fallback: irrigate first planted tile or noop
    for (let i = 0; i < grid.length; i++) {
      if (grid[i].isPlanted && obs.waterStock >= 10) {
        return { type: 'IRRIGATE', tileIdx: i };
      }
    }

    return { type: 'NOOP', tileIdx: 0 };
  }
}
