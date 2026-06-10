import json
import os
import urllib.request
import urllib.error

def handler(request):
    if request.method == "OPTIONS":
        from flask import Response
        return Response("", 200)

    body = request.get_json(force=True, silent=True) or {}

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return json.dumps({"error": "ANTHROPIC_API_KEY not set"}), 500, {"Content-Type": "application/json"}

    prompt = (
        f"You are a senior F1 race strategist. Give a race strategy briefing.\n\n"
        f"Circuit: {body.get('circuit_name')} | Laps: {body.get('total_laps')} | "
        f"Track: {body.get('track_temp')}C | Weather: {body.get('weather')}\n"
        f"Starting tyre: {body.get('starting_compound')} | Style: {body.get('style')}\n"
        f"Tyre life: {body.get('eff_life')} laps | Pit window: laps {body.get('pit_window_start')}-{body.get('pit_window_end')}\n"
        f"Optimal strategy: {body.get('best_sequence')} | Pit lap(s): {body.get('best_pits')}\n\n"
        f"Write 5 sections: 1.STRATEGIC OVERVIEW 2.KEY RISKS 3.PIT WINDOW 4.DRIVER NOTES 5.TACTICAL EDGE\n"
        f"Use **bold** for key numbers and compound names."
    )

    payload = json.dumps({
        "model": "claude-opus-4-6",
        "max_tokens": 800,
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
        with urllib.request.urlopen(req, timeout=25) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = "".join(b.get("text", "") for b in result.get("content", []))
            return json.dumps({"briefing": text}), 200, {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8")
        return json.dumps({"error": f"API error {e.code}", "detail": detail}), 500, {"Content-Type": "application/json"}
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {"Content-Type": "application/json"}
