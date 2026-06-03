import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
        except:
            self._respond(400, {"error": "Invalid JSON"})
            return

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            self._respond(500, {"error": "ANTHROPIC_API_KEY not set"})
            return

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
                self._respond(200, {"briefing": text})
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8")
            self._respond(500, {"error": f"Claude API error {e.code}", "detail": body})
        except Exception as e:
            self._respond(500, {"error": str(e)})

    def do_OPTIONS(self):
        self._respond(200, {})

    def _respond(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))
