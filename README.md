# 🏎️ F1 Tyre Degradation Optimizer

A web-based F1 race strategy simulation tool that models tyre degradation across a race and calculates the optimal pit stop strategy, powered by physics-based simulation and AI analysis.

---

## 📌 About The Project:
Formula 1 race strategy is one of the most complex and high-stakes decision-making environments in sport. This project presents an interactive tyre degradation optimizer that simulates real-world tyre behaviour across a race distance, calculates every valid pit stop strategy, and delivers a professional race engineer-style briefing powered by the Claude AI API.

---

## ⚠️ Problem:
- F1 tyre strategy involves dozens of variables — track temperature, fuel load, driving style, compound choice — making it difficult to understand without engineering tools.
- Fans and enthusiasts have no accessible way to simulate "what if" race scenarios or understand why teams make specific pit stop decisions.
- There is no simple tool that combines tyre physics simulation with AI-generated strategy interpretation in one place.

## 💡 Solution:
- A physics-based simulation engine models tyre degradation lap-by-lap across all five Pirelli compounds using real F1 parameters.
- A strategy engine brute-forces every valid 1-stop and 2-stop combination and ranks them by total simulated race time.
- The Claude AI API generates a professional pit wall strategy briefing interpreting the simulation results.
- Integrated into a Flask web application with an interactive dashboard interface.

## 📈 Results:
- Simulates full race degradation curves for all 5 tyre compounds
- Evaluates and ranks up to 8 valid pit stop strategies per race
- Covers 10 F1 circuits with circuit-specific characteristics

---

## 🖥️ Screenshots:
<img width="1920" height="828" alt="  (1)" src="https://github.com/user-attachments/assets/7c7766ae-1176-403d-b1cd-eb2d4309657e" />
<img width="1920" height="830" alt="  (2)" src="https://github.com/user-attachments/assets/9b3499a0-01b7-4f66-8b78-3ea0b607c785" />
<img width="1920" height="824" alt="  (3)" src="https://github.com/user-attachments/assets/33c7f77a-313c-4852-b7e0-37a091b39a04" />
<img width="1568" height="580" alt="WhatsApp Image 2026-06-11 at 5 52 55 PM" src="https://github.com/user-attachments/assets/2cf27167-0aff-43b3-a432-216d2696b9b6" />

---

## 💻 The System:
- User selects circuit, weather conditions, tyre compound, fuel load, and driving style
- Physics model calculates lap-by-lap tyre life remaining for all compounds
- Strategy engine evaluates all valid 1-stop and 2-stop sequences
- Results displayed as degradation curves, lap time delta charts, strategy table, and wear simulator
- Claude AI generates a 5-section race engineer briefing based on simulation output

---

## 🧠 How The Simulation Works:
1. User sets race parameters — circuit, track temp, weather, fuel, driving style
2. Degradation model applies temperature, fuel weight, humidity, and style multipliers per lap
3. Two-phase degradation simulates tyre warmup then full wear rate
4. Thermal runaway effect modelled below 20% tyre life (the "cliff")
5. Strategy engine tests every compound combination across valid pit windows
6. Total race time calculated as sum of all lap times plus 22-second pit stop penalty
7. Strategies ranked by fastest total time — optimal highlighted
8. Claude AI interprets results as a structured pit wall briefing

---

## 🛠️ Tech Stack:

|     Layer      |                Technology                     |
|----------------|-----------------------------------------------|
| Backend        | Python 3, Flask                               |
| AI Integration | Anthropic Claude API                          |
| Frontend       | HTML5, CSS3, Vanilla JavaScript               |
| Charts         | Chart.js                                      |
| Fonts          | Google Fonts (Rajdhani, IBM Plex Mono, Inter) |
| IDE            | Visual Studio Code                            |

---

## 📁 Project Structure:
```
f1-tyre-optimizer/
├── app.py                  ← Flask backend & AI strategy API
├── requirements.txt        ← Python dependencies
├── Procfile                ← Process declaration for deployment
├── render.yaml             ← Render deployment configuration
├── vercel.json             ← Vercel deployment configuration
├── .gitignore
├── README.md
├── api/
│   └── strategy.py         ← Serverless AI strategy function
└── templates/
    └── index.html          ← Full frontend (single-page app)
```

---

## ✅ Features:

|       Feature      |               Description                                                            |
|--------------------|--------------------------------------------------------------------------------------|
| Degradation Curve  | Lap-by-lap tyre life chart for all 5 compounds                                       |
| Lap Pace Tab       | Time loss per lap vs fresh tyre for selected compound                                |
| Pit Strategy Table | All valid strategies ranked by total race time                                       |
| Wear Simulator     | Drag-slider to see tyre wear state at any lap                                        |
| AI Briefing        | Claude-powered race engineer strategy analysis                                       |
| 10 Circuits        | Monaco, Silverstone, Monza, Spa, Suzuka, Bahrain, Singapore, Mexico, COTA, Abu Dhabi |
| 5 Compounds        | Soft, Medium, Hard, Intermediate, Wet                                                |
| 4 Driving Styles   | Conservative, Balanced, Aggressive, Max Attack                                       |

---

## 📊 Simulation Model Details:

|      Parameter      |             Details                            |
|---------------------|------------------------------------------------|
| Compounds           | Soft, Medium, Hard, Intermediate, Wet          |
| Degradation Factors | Track temp, fuel load, humidity, driving style |
| Tyre Life (Soft)    | ~25 laps baseline                              |
| Tyre Life (Medium)  | ~38 laps baseline                              |
| Tyre Life (Hard)    | ~55 laps baseline                              |
| Pit Stop Penalty    | 22 seconds per stop                            |
| Thermal Runaway     | Modelled below 20% tyre life                   |
| Strategy Types      | 1-stop and 2-stop combinations                 |

---

## ⚠️ Disclaimer:
This application is developed for **academic and educational purposes only**.
The simulation uses publicly known F1 tyre behaviour parameters and is **not based on official Pirelli or FIA data**. Results are for entertainment and learning purposes and should not be used for actual race strategy decisions.

---

## 👩‍💻 Developed By:

*K. Sailaja*  
B.Tech — Computer Science & Engineering   
Batch: 2022–2026
