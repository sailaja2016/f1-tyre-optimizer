import json
import os
import urllib.request
import urllib.error

def handler(request):
    if request.method == "OPTIONS":
        return Response("", 200, {"Access-Control-Allow-Origin": "*",
                                   "Access-Control-Allow-Methods": "POST",
                                   "Access-Control-Allow-Headers": "Content-Type"})

    if request.method != "POST":
        return Response(json.dumps({"error": "Method not allowed"}), 405,
                       {"Content-Type": "application/json"})

    try:
        data = request.json
    except Exception:
        return Response(json.dumps({"error": "Invalid JSON"}), 400,
                       {"Content-Type": "application/json"})

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return Response(json.dumps({"error": "ANTHROPIC_API_KEY not set"}), 500,
                       {"Content-Type": "application/json"})

    prompt = f"""You are a senior F1 race strategist on the pit wall. Provide a sharp, data-driven race strategy briefing.

CIRCUIT: {data.get('circuit_name')} ({data.get('circuit_country')})
Circuit type: {data.get('circuit_type')} | Abrasion: {data.get('abrasion')}
Race distance: {data.get('total_laps')} laps

CONDITIONS:
- Track: {data.get('track_temp')}C | Air: {data.get('air_temp')}C | Humidity: {data.get('humidity')}%
- Weather: {data.get('weather')}
- Fuel: {data.get('fuel')}kg | Pressure: {data.get('pressure')}psi
- Driver style: {data.get('style')}

TYRE ANALYSIS:
- Starting compound: {data.get('starting_compound')}
- Estimated tyre life: {data.get('eff_life')} laps
- Pit window: Laps {data.get('pit_window_start')} to {data.get('pit_window_end')}

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
            return Response(json.dumps({"briefing": text}), 200,
                           {"Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*"})
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return Response(json.dumps({"error": f"Claude API error {e.code}", "detail": err_body}),
                       500, {"Content-Type": "application/json"})
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), 500,
                       {"Content-Type": "application/json"})


class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status_code = status
        self.headers = headers or {}
