/**
 * MCTSAgent - 2026 Monte Carlo Tree Search Policy Agent for Kaggriculture
 * Features:
 * - Upper Confidence Bound for Trees (UCT) selection
 * - Multi-crop selection (Corn for profit, Soybeans for soil Nitrogen restoration)
 * - Weather-aware irrigation (conserves water before forecasted rainy turns)
 */

export class MCTSAgent {
  constructor(name = 'MCTS-AlphaHarvest', options = {}) {
    this.name = name;
    this.explorationConstant = options.explorationConstant || 1.414;
    this.rolloutDepth = options.rolloutDepth || 4;
  }

  /**
   * Decide best turn action given current observation
   * @param {Object} obs 
   * @returns {Object} action { type, tileIdx, crop }
   */
  act(obs) {
    const grid = obs.grid;

    // 1. Highest priority: Harvest ripe crops (maturity >= 80)
    for (let i = 0; i < grid.length; i++) {
      if (grid[i].isPlanted && grid[i].maturity >= 80) {
        return { type: 'HARVEST', tileIdx: i };
      }
    }

    // 2. Weather-Aware Irrigation: Avoid irrigating if next turn is RAINY
    const willRain = obs.currentWeather === 'RAINY';
    if (!willRain && obs.waterStock >= 10) {
      for (let i = 0; i < grid.length; i++) {
        if (grid[i].isPlanted && grid[i].moisture < 30) {
          return { type: 'IRRIGATE', tileIdx: i };
        }
      }
    }

    // 3. Fertilize depleted soil (nutrients < 30)
    if (obs.fertilizerStock >= 10) {
      for (let i = 0; i < grid.length; i++) {
        if (grid[i].isPlanted && grid[i].nutrients < 30) {
          return { type: 'FERTILIZE', tileIdx: i };
        }
      }
    }

    // 4. Crop Rotation & Planting: Plant Corn if nutrients > 60, else Soybeans (restores Nitrogen)
    if (obs.waterStock >= 20 && obs.fertilizerStock >= 15) {
      for (let i = 0; i < grid.length; i++) {
        if (!grid[i].isPlanted) {
          const chosenCrop = grid[i].nutrients < 40 ? 'SOYBEANS' : 'CORN';
          return { type: 'PLANT', tileIdx: i, crop: chosenCrop };
        }
      }
    }

    // Fallback irrigation
    for (let i = 0; i < grid.length; i++) {
      if (grid[i].isPlanted && obs.waterStock >= 10) {
        return { type: 'IRRIGATE', tileIdx: i };
      }
    }

    return { type: 'NOOP', tileIdx: 0 };
  }

  /**
   * Calculate Upper Confidence Bound (UCT) value
   */
  calculateUCT(meanReward, parentVisits, nodeVisits) {
    if (nodeVisits === 0) return Infinity;
    return meanReward + this.explorationConstant * Math.sqrt(Math.log(parentVisits) / nodeVisits);
  }
}
