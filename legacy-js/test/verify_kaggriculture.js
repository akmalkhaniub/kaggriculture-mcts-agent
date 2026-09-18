import assert from 'assert';
import { AgriculturalSimEnv } from '../src/agricultural_sim_env.js';
import { MCTSAgent } from '../src/mcts_agent.js';

console.log('🧪 Starting Kaggriculture Simulation Automated Verification Suite (Kaggle 2026)...\n');

const env = new AgriculturalSimEnv({ gridSize: 4, maxTurns: 25 });
const agent = new MCTSAgent('MCTS-AlphaHarvest');

console.log('1️⃣ Initializing 4x4 Agricultural Environment...');
let obs = env.reset();
assert(obs.grid.length === 16, 'Should have 16 tiles');
assert(obs.waterStock === 100, 'Initial water should be 100');
assert(obs.fertilizerStock === 50, 'Initial fertilizer should be 50');
assert(obs.sustainabilityIndex === 100, 'Sustainability index starts at 100');
console.log(`   ✅ Grid initialized: 16 plots, Water: ${obs.waterStock} units, Fertilizer: ${obs.fertilizerStock} units, Weather: ${obs.currentWeather}.`);

console.log('2️⃣ Running 25-Turn Competitive Agricultural Simulation...');
let turnCount = 0;
let totalHarvests = 0;

while (turnCount < 25) {
  const action = agent.act(obs);
  if (action.type === 'HARVEST') totalHarvests++;

  const stepResult = env.step(action);
  obs = stepResult.observation;
  turnCount++;

  if (stepResult.reward > 0) {
    console.log(`   🌾 Turn ${turnCount}: [${action.type} Tile #${action.tileIdx}] Harvested yield worth +$${stepResult.reward}! (Weather: ${obs.currentWeather})`);
  }
}

console.log(`\n3️⃣ Evaluating End-of-Season Performance Metrics:`);
console.log(`   • Total Completed Turns: ${obs.turn} / ${obs.maxTurns}`);
console.log(`   • Successful Harvest Operations: ${totalHarvests}`);
console.log(`   • Total Commercial Revenue Generated: $${obs.totalRevenue}`);
console.log(`   • Environmental Sustainability Index: ${obs.sustainabilityIndex} / 100`);
console.log(`   • Remaining Water Reserves: ${obs.waterStock} units`);

assert(obs.totalRevenue > 0, 'Agent must successfully generate harvest revenue');
assert(totalHarvests >= 2, 'Agent must successfully execute multiple harvest cycles');
assert(obs.sustainabilityIndex >= 70, 'Sustainability index must remain high');

// Test 4: MCTS UCT Calculation Verification
console.log('\n4️⃣ Testing MCTS UCT (Upper Confidence Bound) Formula...');
const uctVal = agent.calculateUCT(140.0, 100, 10);
assert(typeof uctVal === 'number' && uctVal > 140.0, 'UCT value must balance reward and exploration');
console.log(`   ✅ MCTS UCT Value (Q=140, N_p=100, N_c=10): ${uctVal.toFixed(2)}`);

console.log('\n🎉 ALL KAGGRICULTURE SIMULATION TESTS PASSED WITH 100% SUCCESS!\n');
