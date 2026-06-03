from flask import Flask, render_template, jsonify, request
import os
import json
import urllib.request
import urllib.error

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/strategy", methods=["POST"])
def strategy():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    data = request.get_json()

    prompt = f"""You are a senior F1 race strategist on the pit wall. Provide a sharp, data-driven race strategy briefing.

CIRCUIT: {data.get('circuit_name')} ({data.get('circuit_country')})
Circuit type: {data.get('circuit_type')} | Abrasion: {data.get('abrasion')}
Race distance: {data.get('total_laps')} laps

CONDITIONS:
- Track: {data.get('track_temp')}°C | Air: {data.get('air_temp')}°C | Humidity: {data.get('humidity')}%
- Weather: {data.get('weather')}
- Fuel: {data.get('fuel')}kg | Pressure: {data.get('pressure')}psi
- Driver style: {data.get('style')}

TYRE ANALYSIS:
- Starting compound: {data.get('starting_compound')}
- Estimated tyre life: {data.get('eff_life')} laps
- Pit window: Laps {data.get('pit_window_start')}–{data.get('pit_window_end')}

OPTIMAL STRATEGY: {data.get('best_sequence')}
Pit stop laps: {data.get('best_pits')}
Strategies evaluated: {data.get('strategies_count')}

Provide a structured briefing:
1. STRATEGIC OVERVIEW (2 sentences)
2. KEY RISKS (bullet points)
3. PIT WINDOW RECOMMENDATION (with reasoning)
4. DRIVER NOTES
5. TACTICAL EDGE

Use ** around key numbers and compound names. Write like a real pit wall engineer."""

    payload = json.dumps({
        "model": "claude-opus-4-6",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(b.get("text", "") for b in result.get("content", []))
            return jsonify({"briefing": text})
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return jsonify({"error": f"Claude API error: {e.code}", "detail": body}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
