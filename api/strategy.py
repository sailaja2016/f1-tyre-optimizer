import json, os, urllib.request, urllib.error
from flask import Response, request

def handler(req=None):
    try:
        data = json.loads(request.data)
    except:
        data = {}

    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return Response(json.dumps({"error": "no key"}), status=500, mimetype="application/json")

    prompt = (
        "You are an F1 race strategist. Give a 5-section briefing.\n"
        f"Circuit: {data.get('circuit_name')}, {data.get('total_laps')} laps, "
        f"{data.get('track_temp')}C, {data.get('weather')} weather.\n"
        f"Tyre: {data.get('starting_compound')}, style: {data.get('style')}.\n"
        f"Pit window: laps {data.get('pit_window_start')}-{data.get('pit_window_end')}.\n"
        f"Best strategy: {data.get('best_sequence')}, pit lap {data.get('best_pits')}.\n"
        "Sections: 1.STRATEGIC OVERVIEW 2.KEY RISKS 3.PIT WINDOW 4.DRIVER NOTES 5.TACTICAL EDGE\n"
        "Use **bold** for key numbers and compound names."
    )

    payload = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800
    }).encode()

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "Mozilla/5.0 (compatible; F1TyreOptimizer/1.0)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            result = json.loads(r.read())
            text = result["choices"][0]["message"]["content"]
            return Response(json.dumps({"briefing": text}), status=200, mimetype="application/json")
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        return Response(json.dumps({"error": str(e.code), "detail": err}), status=500, mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")
