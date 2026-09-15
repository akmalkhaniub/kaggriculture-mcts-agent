/**
 * AgriculturalSimEnv - Agricultural Simulation Game Environment
 * Models soil moisture, nutrient dynamics, crop maturity stages, and environmental fluctuations.
 */

export class AgriculturalSimEnv {
  constructor(options = {}) {
    this.gridSize = options.gridSize || 4; // 4x4 agricultural plots
    this.maxTurns = options.maxTurns || 30;
    this.reset();
  }

  reset() {
    this.currentTurn = 0;
    this.revenue = 0;
    this.waterStock = 100;
    this.fertilizerStock = 50;

    // Grid state: Array of { moisture, nutrients, maturity, isPlanted }
    this.grid = Array.from({ length: this.gridSize * this.gridSize }, () => ({
      moisture: 50,    // 0-100
      nutrients: 50,   // 0-100
      maturity: 0,     // 0-100 (100 = ready to harvest)
      isPlanted: false
    }));

    return this.getObservation();
  }

  getObservation() {
    return {
      turn: this.currentTurn,
      maxTurns: this.maxTurns,
      waterStock: this.waterStock,
      fertilizerStock: this.fertilizerStock,
      totalRevenue: this.revenue,
      grid: this.grid.map(tile => ({ ...tile }))
    };
  }

  /**
   * Execute action: { type: 'PLANT'|'IRRIGATE'|'FERTILIZE'|'HARVEST', tileIdx: number }
   */
  step(action) {
    let turnReward = 0;
    const tile = this.grid[action.tileIdx];

    if (tile) {
      if (action.type === 'PLANT' && !tile.isPlanted) {
        tile.isPlanted = true;
        tile.maturity = 10;
      } else if (action.type === 'IRRIGATE' && this.waterStock >= 10) {
        this.waterStock -= 10;
        tile.moisture = Math.min(100, tile.moisture + 30);
      } else if (action.type === 'FERTILIZE' && this.fertilizerStock >= 10) {
        this.fertilizerStock -= 10;
        tile.nutrients = Math.min(100, tile.nutrients + 30);
      } else if (action.type === 'HARVEST' && tile.isPlanted && tile.maturity >= 80) {
        const yieldValue = Math.round(tile.maturity * 1.5);
        this.revenue += yieldValue;
        turnReward += yieldValue;
        tile.isPlanted = false;
        tile.maturity = 0;
      }
    }

    // Natural environment decay & crop growth
    for (const t of this.grid) {
      if (t.isPlanted) {
        if (t.moisture >= 30 && t.nutrients >= 30) {
          t.maturity = Math.min(100, t.maturity + 25);
        }
        t.moisture = Math.max(0, t.moisture - 15);
        t.nutrients = Math.max(0, t.nutrients - 10);
      }
    }

    this.currentTurn++;
    const isDone = this.currentTurn >= this.maxTurns;

    return {
      observation: this.getObservation(),
      reward: turnReward,
      done: isDone
    };
  }
}
