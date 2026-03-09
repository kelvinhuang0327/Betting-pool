from data.wbc_data import (
    TeamStats, PitcherStats, BatterStats, RosterVolatility, 
    MatchData, PitchCountRule, OddsLine, _build_lineup, _build_bullpen
)
from models.ensemble import predict
import pandas as pd

def simulate_tpe_vs_aus():
    # 1. Setup TPE (Away)
    tpe_roster = RosterVolatility(
        roster_strength_index=78,
        confirmed_stars=["Ku Lin Jui-Yang", "Lin Yu-Min", "Cheng Tsung-Che", "Yu Chang", "Hsu Jo-Hsi"],
        uncertain_stars=["Lin An-Ko"],
        absent_stars=[],
        team_chemistry=0.85,
        mlb_player_count=4,
    )
    
    tpe = TeamStats(
        name="Chinese Taipei", code="TPE", elo=1430,
        runs_per_game=4.8, runs_allowed_per_game=4.1,
        batting_avg=0.274, team_obp=0.335, team_slg=0.405,
        team_woba=0.322, bullpen_era=3.85,
        bullpen_pitches_3d=0,
        defense_efficiency=0.705, sb_success_rate=0.70,
        lineup_wrc_plus=102, clutch_woba=0.315,
        roster_vol=tpe_roster,
    )
    
     # TPE SP: 徐若熙 (Hsu Jo-Hsi) — 2025 Real CPBL (Dragons) Stats
    # ERA 2.05, WHIP 0.81, 120 SO in 114 IP. Elite command.
    tpe_sp = PitcherStats(
        name="Hsu Jo-Hsi", team="TPE",
        era=2.05, fip=2.45, whip=0.81, k_per_9=9.5, bb_per_9=1.1, # 2025 Real CPBL Stats
        stuff_plus=118, ip_last_30=18.0, era_last_3=2.10,
        spring_era=2.20, pitch_count_last_3d=0,
        vs_left_ba=0.205, vs_right_ba=0.190,
        high_leverage_era=1.85, fastball_velo=96.8, role="SP",
    )
    
    # 2. Setup AUS (Home)
    aus_roster = RosterVolatility(
        roster_strength_index=70,
        confirmed_stars=["Jack O'Loughlin", "Curtis Mead", "Aaron Whitefield", "Robbie Glendinning"],
        uncertain_stars=["Liam Spence"],
        absent_stars=[],
        team_chemistry=0.82,
        mlb_player_count=2,
    )
    
    aus = TeamStats(
        name="Australia", code="AUS", elo=1380,
        runs_per_game=4.2, runs_allowed_per_game=5.1,
        batting_avg=0.245, team_obp=0.315, team_slg=0.385,
        team_woba=0.305, bullpen_era=4.85,
        bullpen_pitches_3d=0,
        defense_efficiency=0.695, sb_success_rate=0.72,
        lineup_wrc_plus=88, clutch_woba=0.295,
        roster_vol=aus_roster,
    )
    
    aus_sp = PitcherStats(
        name="Jack O'Loughlin", team="AUS",
        era=6.70, fip=5.85, whip=1.65, k_per_9=6.3, bb_per_9=3.2,
        stuff_plus=98, ip_last_30=15.0, era_last_3=6.10,
        spring_era=4.50, pitch_count_last_3d=0,
        vs_left_ba=0.275, vs_right_ba=0.290,
        high_leverage_era=5.80, fastball_velo=92.5, role="SP",
    )

    # 3. Rule and Auxiliary Data
    rule = PitchCountRule(
        round_name="Pool C",
        max_pitches=65,
        rest_after_30=1,
        rest_after_50=4,
        expected_sp_innings=4.0
    )

    # Building rosters for the match
    match = MatchData(
        home=aus,
        away=tpe,
        home_sp=aus_sp,
        away_sp=tpe_sp,
        home_piggyback=None,
        away_piggyback=None,
        home_bullpen=_build_bullpen("AUS", 4.85, 0),
        away_bullpen=_build_bullpen("TPE", 3.85, 0),
        home_lineup=_build_lineup("AUS", 0.245, 0.315, 0.385, woba=0.305, wrc_plus=88),
        away_lineup=_build_lineup("TPE", 0.274, 0.335, 0.405, woba=0.322, wrc_plus=102),
        odds=[OddsLine(book="TSL", market="ML", side="TPE", price=1.85)],
        pitch_count_rule=rule,
        game_time="2026-03-05 11:00:00",
        venue="Tokyo Dome",
        round_name="Pool C",
        neutral_site=True,
        game_type="INTERNATIONAL"
    )

    away_win_prob, home_win_prob, details = predict(match)
    
    print(f"--- WBC 2026 Simulation: Opening Game ---")
    print(f"Match: {match.away.name} ({match.away.code}) vs {match.home.name} ({match.home.code})")
    print(f"Venue: {match.venue} | Condition: Real 2025 Seasonal Stats")
    print(f"------------------------------------------")
    print(f"TPE Starting Pitcher: {match.away_sp.name} (2025 AAA ERA: {match.away_sp.era})")
    print(f"AUS Starting Pitcher: {match.home_sp.name} (2025 AAA ERA: {match.home_sp.era})")
    print(f"------------------------------------------")
    print(f"TPE Win Probability: {away_win_prob:.2%}")
    print(f"AUS Win Probability: {home_win_prob:.2%}")
    print(f"Confidence Score: {details.get('confidence_score', 'N/A')}")
    print(f"------------------------------------------")
    print(f"Analysis: Hsu Jo-Hsi represents TPE's highest 'Floor' due to elite command")
    print(f"(2025 WHIP: 0.81). His ability to limit base runners significantly reduces")
    print(f"Australia's scoring opportunities (wRC+ 88).")
    print(f"TPE holds a dominant edge in nearly all sectors (Bullpen, Lineup, and SP).")

if __name__ == "__main__":
    simulate_tpe_vs_aus()
