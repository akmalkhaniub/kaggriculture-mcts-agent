import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { AgriculturalSimEnv } from './agricultural_sim_env.js';
import { MCTSAgent } from './mcts_agent.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PUBLIC_DIR = path.join(__dirname, 'public');
const PORT = process.env.PORT || 3010;

let env = new AgriculturalSimEnv({ gridSize: 4, maxTurns: 30 });
const agent = new MCTSAgent('MCTS-AlphaHarvest');

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Health check endpoint for container probes & cloud orchestrators
  if (req.url === '/api/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'online',
      service: 'Kaggriculture MCTS Agent',
      timestamp: new Date().toISOString()
    }));
    return;
  }

  // REST API Routes
  if (req.url === '/api/state' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(env.getObservation()));
    return;
  }

  if (req.url === '/api/step' && req.method === 'POST') {
    const obs = env.getObservation();
    if (obs.turn >= obs.maxTurns) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ done: true, observation: obs }));
      return;
    }

    const action = agent.act(obs);
    const result = env.step(action);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ action, ...result }));
    return;
  }

  if (req.url === '/api/reset' && req.method === 'POST') {
    env = new AgriculturalSimEnv({ gridSize: 4, maxTurns: 30 });
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(env.getObservation()));
    return;
  }

  // Static files
  let filePath = path.join(PUBLIC_DIR, req.url === '/' ? 'index.html' : req.url);
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8'
  };

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Server Error: ' + err.code);
      }
    } else {
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log(`🌾 Kaggriculture Server running at http://localhost:${PORT}`);
});
