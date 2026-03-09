
import urllib.request
import json
import os

def fetch_wbc_stats(group):
    # groups: pitching, hitting
    url = f"https://statsapi.mlb.com/api/v1/stats?stats=season&group={group}&sportId=51&season=2023"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"Fetching WBC {group} stats from: {url}")
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            stats = data.get('stats', [])
            if stats:
                splits = stats[0].get('splits', [])
                print(f"Found {len(splits)} player stats for {group}.")
                
                output_file = f"/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_{group}_stats_2026.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"Saved {group} stats to {output_file}")
            else:
                print(f"No stats found for {group}.")
    except Exception as e:
        print(f"Error fetching {group} stats: {e}")

if __name__ == "__main__":
    fetch_wbc_stats("pitching")
    fetch_wbc_stats("hitting")
