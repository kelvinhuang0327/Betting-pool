import pandas as pd
import numpy as np

def calculate_betting_value(model_prob_win, bookmaker_odds, book_name="Bookmaker"):
    """
    Calculates Edge and Implied Probability for a single outcome.
    """
    implied_prob = 1 / bookmaker_odds
    edge = (model_prob_win * bookmaker_odds) - 1
    
    return {
        "Book": book_name,
        "Market Odds": bookmaker_odds,
        "Implied Prob": f"{implied_prob:.2%}",
        "Model Prob": f"{model_prob_win:.2%}",
        "EV (Edge)": f"{edge:.2%}",
        "Status": "VALUE" if edge > 0 else "NO VALUE"
    }

def find_arbitrage(odds_away, odds_home):
    """
    Checks for arbitrage between two different bookmakers.
    """
    arbitrage_sum = (1 / odds_away) + (1 / odds_home)
    is_arbitrage = arbitrage_sum < 1
    profit_margin = (1 - arbitrage_sum) * 100 if is_arbitrage else 0
    
    return {
        "Arbitrage Sum": f"{arbitrage_sum:.4f}",
        "Is Arbitrage": "YES" if is_arbitrage else "NO",
        "Profit Margin": f"{profit_margin:.2f}%"
    }

def generate_wbc_strategy_report(tpe_win_prob, aus_win_prob):
    # Simulated Odds based on market research (TSL vs International)
    # Market seems to think it's a toss-up (~1.85 each) or slightly favors AUS
    market_scenarios = [
        {"Book": "TSL (Estimated)", "TPE_ML": 1.75, "AUS_ML": 1.85},
        {"Book": "Pinnacle (Estimated)", "TPE_ML": 2.05, "AUS_ML": 1.75},
        {"Book": "Bet365 (Estimated)", "TPE_ML": 1.80, "AUS_ML": 1.80},
    ]
    
    print("--- WBC 2026 Arbitrage & Value Analysis: TPE vs AUS ---")
    print(f"Model Data: Hsu Jo-Hsi (TPE) vs J. O'Loughlin (AUS)")
    print(f"Prediction: TPE {tpe_win_prob:.2%}, AUS {aus_win_prob:.2%}")
    print("-" * 60)
    
    results = []
    for scenario in market_scenarios:
        val_tpe = calculate_betting_value(tpe_win_prob, scenario["TPE_ML"], f"{scenario['Book']} - TPE")
        results.append(val_tpe)
        
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    
    print("-" * 60)
    print("--- Cross-Market Arbitrage Discovery ---")
    # Checking for Arbitrage between TSL (TPE) and Pinnacle (AUS)
    arb = find_arbitrage(1.75, 1.75) # Worst case
    print(f"TSL (TPE 1.75) vs Pinny (AUS 1.75): Sum {arb['Arbitrage Sum']} | {arb['Is Arbitrage']}")
    
    # Checking for Arbitrage between Pinnacle (TPE 2.05) and TSL (AUS 1.85)
    arb2 = find_arbitrage(2.05, 1.85)
    print(f"Pinny (TPE 2.05) vs TSL (AUS 1.85): Sum {arb2['Arbitrage Sum']} | {arb2['Is Arbitrage']} | Margin: {arb2['Profit Margin']}")

if __name__ == "__main__":
    # Using the 85.91% win prob for the Hsu Jo-Hsi case
    generate_wbc_strategy_report(0.8591, 0.1409)
