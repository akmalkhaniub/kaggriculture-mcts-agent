/**
 * AgriculturalSimEnv - 2026 Kaggle Digital Twin Environment
 * Features:
 * - Multi-crop mechanics: Wheat, Corn, and Nitrogen-Fixing Soybeans
 * - Stochastic Weather: SUNNY, RAINY (+20 moisture), DROUGHT (-25 moisture)
 * - Soil Health & Environmental Sustainability Scoring (fertilizer runoff penalty)
 */

export const CROPS = {
  WHEAT: { name: 'Wheat', yieldValue: 120, waterReq: 25, nutrientReq: 20 },
  CORN: { name: 'Corn', yieldValue: 180, waterReq: 35, nutrientReq: 30 },
  SOYBEANS: { name: 'Soybeans', yieldValue: 140, waterReq: 20, nutrientReq: 10, fixesNitrogen: true }
};

export class AgriculturalSimEnv {
  constructor(options = {}) {
    this.gridSize = options.gridSize || 4; // 4x4 agricultural plots
    this.maxTurns = options.maxTurns || 30;
    this.weatherStates = ['SUNNY', 'RAINY', 'SUNNY', 'DROUGHT', 'SUNNY'];
    this.reset();
  }

  reset() {
    this.currentTurn = 0;
    this.revenue = 0;
    this.waterStock = 100;
    this.fertilizerStock = 50;
    this.currentWeather = 'SUNNY';
    this.environmentalRunoff = 0;

    // Grid state: Array of { moisture, nutrients, maturity, isPlanted, cropType }
    this.grid = Array.from({ length: this.gridSize * this.gridSize }, () => ({
      moisture: 50,    // 0-100
      nutrients: 50,   // 0-100
      maturity: 0,     // 0-100 (100 = ready to harvest)
      isPlanted: false,
      cropType: null
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
      currentWeather: this.currentWeather,
      environmentalRunoff: this.environmentalRunoff,
      sustainabilityIndex: Math.max(0, 100 - Math.round(this.environmentalRunoff * 1.2)),
      grid: this.grid.map(tile => ({ ...tile }))
    };
  }

  /**
   * Execute action: { type: 'PLANT'|'IRRIGATE'|'FERTILIZE'|'HARVEST'|'NOOP', tileIdx: number, crop: string }
   */
  step(action) {
    let turnReward = 0;
    const tile = this.grid[action.tileIdx];

    // 1. Weather transition
    this.currentWeather = this.weatherStates[this.currentTurn % this.weatherStates.length];

    if (tile) {
      if (action.type === 'PLANT' && !tile.isPlanted) {
        const cropKey = action.crop || 'WHEAT';
        tile.isPlanted = true;
        tile.cropType = cropKey;
        tile.maturity = 10;
      } else if (action.type === 'IRRIGATE' && this.waterStock >= 10) {
        this.waterStock -= 10;
        tile.moisture = Math.min(100, tile.moisture + 30);
      } else if (action.type === 'FERTILIZE' && this.fertilizerStock >= 10) {
        this.fertilizerStock -= 10;
        tile.nutrients = Math.min(100, tile.nutrients + 30);
        // Excess fertilizer when moisture is high creates runoff
        if (tile.moisture > 70) {
          this.environmentalRunoff += 5;
        }
      } else if (action.type === 'HARVEST' && tile.isPlanted && tile.maturity >= 80) {
        const crop = CROPS[tile.cropType] || CROPS.WHEAT;
        const yieldValue = Math.round((tile.maturity / 100) * crop.yieldValue);
        this.revenue += yieldValue;
        turnReward += yieldValue;
        
        // Soil effect: Soybeans fix nitrogen!
        if (crop.fixesNitrogen) {
          tile.nutrients = Math.min(100, tile.nutrients + 20); // Crop rotation benefit
        }

        tile.isPlanted = false;
        tile.cropType = null;
        tile.maturity = 0;
      }
    }

    // Natural environment decay & crop growth
    const weatherMoistureDelta = this.currentWeather === 'RAINY' ? 20 : (this.currentWeather === 'DROUGHT' ? -25 : -15);

    for (const t of this.grid) {
      if (t.isPlanted) {
        if (t.moisture >= 25 && t.nutrients >= 25) {
          t.maturity = Math.min(100, t.maturity + 25);
        }
        t.moisture = Math.max(0, Math.min(100, t.moisture + weatherMoistureDelta));
        t.nutrients = Math.max(0, t.nutrients - 10);
      } else if (this.currentWeather === 'RAINY') {
        t.moisture = Math.min(100, t.moisture + 15);
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
