# 🆓 Free Tier Deployment Guide for Kaggriculture MCTS Agent

Deploy **Kaggriculture MCTS Agent** using **Koyeb Free**, **Render Blueprints**, and **Cloudflare Tunnels**.

---

## 1. Free Web Simulation Host: Koyeb or Render
Deploy the interactive 16-plot farming digital twin with zero cost:
- **Koyeb**: Connect repo and select Docker deployment (`koyeb.yaml`).
- **Render**: Connect repo and select Blueprint (`render.yaml`).

---

## 2. Remote Live Demo: Cloudflare Tunnel
```powershell
# Windows
.\deploy\free\tunnel.ps1 -Port 3010

# Linux / macOS
./deploy/free/tunnel.sh 3010
```
Open the generated `https://*.trycloudflare.com` URL to show real-time MCTS crop rotation decisions!
