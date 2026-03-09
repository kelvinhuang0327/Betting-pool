import urllib.request
import json
import ssl

url = "https://www.sportslottery.com.tw/api/v1/game/list"
payload = {"sportId": "1", "marketGroupId": "0", "lan": "zh-TW"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://www.sportslottery.com.tw",
    "Referer": "https://www.sportslottery.com.tw/zh-tw/game/pre-match?sportId=1"
}

try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        raw = response.read()
        print("Raw len:", len(raw))
        try:
            js = json.loads(raw)
            games = js.get("data", [])
            print("Found Games:", len(games))
            for g in games[:5]:
                print(g.get("awayTeam", {}).get("nameT"), "vs", g.get("homeTeam", {}).get("nameT"))
                markets = g.get("markets", [])
                for m in markets[:3]:
                    print("-", m.get("nameT"), m.get("selections", []))
        except Exception as e:
            print("JSON parse error:", e, raw[:100])
except Exception as e:
    print("Error:", e)
