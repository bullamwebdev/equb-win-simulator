# 🎯 Equb Distribution Win Simulator

A full-stack web application simulating the Ethiopian **Equb ROSCA** (Rotating Savings & Credit Association) raffle system with probability distribution engine, Monte Carlo cascade simulation, and win-rate optimizer.

## 🚀 Live Demo

Hosted via GitHub Pages (frontend) + backend on your server.

---

## 📐 Mathematical Model

| Formula | Description |
|---|---|
| `P(win) = 1/N` | Single raffle win probability |
| `Wins ~ Binomial(M, 1/N)` | Win distribution across M raffles |
| `E[first win] = Σ((N-k)/N)^M` | Expected first win round |
| `P(Round 1 win) = 1-(1-1/N)^M` | Probability of winning in round 1 |
| `Break-even: wins ≥ M/N` | Minimum wins to not lose money |
| `Optimal zone: M = 4N–5N` | Strategy score peaks here |

---

## 🛠 Tech Stack

- **Backend**: Python 3.11 + FastAPI + NumPy + SciPy
- **Frontend**: React 18 + TypeScript + Tailwind CSS + Recharts
- **Deployment**: GitHub Pages (frontend) + Railway/Render (backend)
- **Docker**: Full docker-compose stack

---

## ⚡ Quick Start

```bash
# Clone
git clone https://github.com/bullamwebdev/equb-win-simulator
cd equb-win-simulator

# Run with Docker
docker-compose up --build

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

## 🧪 Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## 💻 Frontend Only

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/simulate` | POST | Run full simulation |
| `/api/optimize` | POST | Find optimal M for target win rate |
| `/api/sweep` | GET | Full parameter grid |
| `/api/export/csv` | GET | Download CSV data |
| `/api/cascade` | POST | Cascade wealth simulation |
| `/docs` | GET | Interactive Swagger UI |

---

## 📊 Features

- **Win Rate Heatmap** — N vs M parameter grid
- **Wealth Simulator** — 5,000 Monte Carlo runs with confidence bands
- **Strategy Matrix** — Bubble chart: risk vs win speed
- **Auto-Optimizer** — Find minimum M for any target win rate
- **Cascade Model** — Self-funding reinvestment pipeline
- **CSV Export** — Full parameter sweep download

---

Built with ❤️ by [bullamwebdev](https://github.com/bullamwebdev)
