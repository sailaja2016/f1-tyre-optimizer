# F1 Tyre Degradation Optimizer

A physics-based F1 tyre strategy simulator with AI race engineer briefings powered by Claude.

---

## What This Project Does

The app simulates tyre behaviour across a race and calculates the optimal pit stop strategy.
It models real-world degradation physics: track temperature, fuel load, driving style,
tyre compound properties, and thermal runaway effects.

---

## How the Prediction Works (Explain to Others)

> "It's a physics-based simulation engine, not a machine learning model. 
> The predictions are built from mathematical models of real F1 tyre behaviour — 
> Pirelli's publicly known tyre operating windows, degradation curves, 
> and the effect of track temperature, fuel weight, and driving style on rubber wear.
> The strategy engine brute-forces every valid 1-stop and 2-stop combination 
> and ranks them by total simulated race time. 
> The AI layer (Claude API) then interprets the results like a real pit wall engineer."

---

## Project Structure

```
f1-tyre-optimizer/
├── app.py                  ← Flask server (serves the HTML template)
├── requirements.txt        ← Python dependencies
├── Procfile                ← Render / Heroku process declaration
├── render.yaml             ← Render auto-deploy configuration
├── vercel.json             ← Vercel deployment configuration
├── .gitignore
├── README.md
└── templates/
    └── index.html          ← The entire app (HTML + CSS + JS in one file)
```

---

## Run Locally

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## Deploy to Vercel (Recommended — Faster & Free)

1. Push this repo to GitHub
2. Go to https://vercel.com → New Project → Import your repo
3. Vercel auto-detects Python/Flask via `vercel.json`
4. Click Deploy — done. Live URL in ~60 seconds.

No environment variables needed unless you add a server-side API key.

---

## Deploy to Render

1. Push this repo to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Render reads `render.yaml` automatically
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Click Deploy

---

## File Size

This app is approximately **35–40 KB** total.
There are no datasets, ML models, or large assets.
The only external dependencies loaded at runtime are:
- Google Fonts (from CDN, ~50KB network)
- Chart.js (from CDN, ~200KB network)

Both are loaded from CDN — they are NOT in this repo and do NOT count toward hosting limits.

---

## Vercel vs Render — Which to Use?

| Feature          | Vercel               | Render               |
|------------------|----------------------|----------------------|
| Speed            | ⚡ Faster (CDN edge) | Moderate             |
| Free tier        | ✅ Very generous     | ✅ Available         |
| Flask support    | ✅ Yes (serverless)  | ✅ Yes (full server) |
| Cold starts      | Yes (serverless)     | Yes (free tier)      |
| Best for         | Static + light API   | Full backends, DBs   |
| Recommendation   | ✅ Use this          | If you add a DB later|

**Use Vercel for this project.**

---

## Tyre Compound Reference

| Compound    | Colour | Life (normal) | Pace vs Soft |
|-------------|--------|---------------|--------------|
| Soft (S)    | Red    | ~25 laps      | Baseline     |
| Medium (M)  | Yellow | ~38 laps      | +0.45s/lap   |
| Hard (H)    | White  | ~55 laps      | +1.1s/lap    |
| Inter (I)   | Green  | ~30 laps      | +2.8s/lap    |
| Wet (W)     | Blue   | ~22 laps      | +5.5s/lap    |

---

## Tech Stack

- **Backend**: Python / Flask
- **Frontend**: Vanilla HTML, CSS, JavaScript (no framework)
- **Charts**: Chart.js (CDN)
- **Fonts**: Google Fonts — Rajdhani, IBM Plex Mono, Inter
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)
- **Deployment**: Vercel (recommended) or Render
