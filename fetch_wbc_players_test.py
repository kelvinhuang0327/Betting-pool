
import urllib.request
import json
import os

def fetch_wbc_players():
    url = "https://statsapi.mlb.com/api/v1/sports/51/players?season=2026"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    print(f"Fetching WBC players from: {url}")
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            players = data.get('people', [])
            print(f"Found {len(players)} players.")
            
            # Save to a file
            output_file = "/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_players_2026.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Saved roster to {output_file}")
            
            return players
    except Exception as e:
        print(f"Error fetching players: {e}")
        return []

if __name__ == "__main__":
    fetch_wbc_players()
