import pandas as pd
import numpy as np
import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from data.wbc_data import fetch_latest_wbc_match, PitcherStats, PitchCountRule
from models import ensemble
from data.mlb_2025_preview import MLB_2025_PREVIEW_META
from data.mlb_2024_pitchers import MLB_2024_PITCHERS
import unicodedata

def normalize_name(name):
    if not isinstance(name, str): return ""
    return "".join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')

TEAM_MAP = {
    "Arizona Diamondbacks": "ARI", "Athletics": "OAK", "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS", "Chicago Cubs": "CHC",
    "Chicago White Sox": "CWS", "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL", "Detroit Tigers": "DET", "Houston Astros": "HOU",
    "Kansas City Royals": "KCR", "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN",
    "New York Mets": "NYM", "New York Yankees": "NYY", "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TBA",
    "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR", "Washington Nationals": "WSN"
}

def american_to_decimal(odds):
    try:
        val = float(odds)
        if val > 0:
            return 1 + (val / 100)
        else:
            return 1 + (100 / abs(val))
    except (ValueError, TypeError):
        return 1.0

def run_compound_simulation(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df = df[df['Status'] == 'Final'].copy()
    df['Away Score'] = pd.to_numeric(df['Away Score'], errors='coerce')
    df['Home Score'] = pd.to_numeric(df['Home Score'], errors='coerce')
    df = df.dropna(subset=['Away Score', 'Home Score'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    start_capital = 200
    current_capital = start_capital
    target_capital = 8000000
    
    streak = 0
    max_streak = 0
    max_capital = start_capital
    total_bets = 0
    wins = 0
    
    # We will simulate multiple "trials" starting from 200
    # Every time we lose, we "restart" with a new 200 (if we have budget, but here we just want to see streaks)
    
    print(f"Starting Compound Betting Simulation...")
    print(f"Goal: Win 20 consecutive bets at ~1.7 odds to reach {target_capital:,}")

    mlb_rule = PitchCountRule(
        round_name="Regular Season", max_pitches=100,
        rest_after_30=0, rest_after_50=0, expected_sp_innings=6.0
    )

    for idx, row in df.iterrows():
        try:
            away_full, home_full = row['Away'], row['Home']
            if away_full not in TEAM_MAP or home_full not in TEAM_MAP: continue
            
            away_code, home_code = TEAM_MAP[away_full], TEAM_MAP[home_full]
            if away_code not in MLB_2025_PREVIEW_META or home_code not in MLB_2025_PREVIEW_META: continue

            away_meta = MLB_2025_PREVIEW_META[away_code]
            home_meta = MLB_2025_PREVIEW_META[home_code]

            match = fetch_latest_wbc_match(live=False)
            match.game_type, match.pitch_count_rule = "PROFESSIONAL", mlb_rule
            match.away.code, match.home.code = away_code, home_code
            match.away.elo, match.home.elo = away_meta["elo"], home_meta["elo"]
            match.away.runs_per_game = away_meta["rpg"]
            match.home.runs_per_game = home_meta["rpg"]
            
            # 1. Predict
            away_wp, home_wp, details = ensemble.predict(match)
            confidence = details.get("confidence_score", 0.0)
            
            # Odds
            odds_away = american_to_decimal(row['Away ML'])
            odds_home = american_to_decimal(row['Home ML'])
            
            # Selection logic: "Sure Bet" (穩膽) criteria
            # Must have high model agreement (>= 66%) AND a decent edge (>= 5%)
            chosen_side = None
            chosen_odds = 0
            
            edge_away = away_wp - (1/odds_away)
            edge_home = home_wp - (1/odds_home)
            
            # Bronze Standard: Confidence >= 0.66 (4/6 models) & Edge >= 0.05
            if confidence >= 0.66:
                if edge_away >= 0.05:
                    chosen_side = "AWAY"
                    chosen_odds = odds_away
                elif edge_home >= 0.05:
                    chosen_side = "HOME"
                    chosen_odds = odds_home
                
            if chosen_side:
                total_bets += 1
                a_score, h_score = row['Away Score'], row['Home Score']
                actual_winner = "HOME" if h_score > a_score else "AWAY"
                
                print(f"Game {total_bets}: {chosen_side} (Conf: {confidence:.2f}, Edge: {max(edge_away, edge_home):.2f}) - {'WIN' if chosen_side == actual_winner else 'LOSS'}")
                if chosen_side == actual_winner:
                    wins += 1
                    streak += 1
                    current_capital *= chosen_odds
                    if streak > max_streak: max_streak = streak
                    if current_capital > max_capital: max_capital = current_capital
                    
                    if current_capital >= target_capital:
                        print(f"!!! TARGET REACHED !!! Streak: {streak} | Capital: {current_capital:,.2f}")
                        break
                else:
                    # Reset
                    streak = 0
                    current_capital = start_capital
                    
        except Exception:
            continue

    print(f"\n--- Simulation Results ---")
    print(f"Total Matches Analyzed: {len(df)}")
    print(f"Total Bets Placed: {total_bets}")
    print(f"Max Consecutive Wins: {max_streak}")
    print(f"Highest Capital Reached: {max_capital:,.2f}")
    if max_capital >= target_capital:
        print(f"Status: SUCCESS - 8 Million goal achieved!")
    else:
        print(f"Status: FAILED - Goal not reached in this sample.")

if __name__ == "__main__":
    file_path = '/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_2025/mlb_odds_2025_real.csv'
    run_compound_simulation(file_path)
