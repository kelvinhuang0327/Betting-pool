"""
Verification Script for Phase 1: Automation.
Tests if TSL Crawler integrates correctly with the main engine.
"""
from data.wbc_data import fetch_latest_wbc_match
from data.tsl_crawler import TSLCrawler
import json

def test_phase_1():
    print("=== Phase 1 Verification: TSL Crawler Integration ===")
    
    # 1. Test Crawler directly (Mock)
    crawler = TSLCrawler(use_mock=True)
    live_match = crawler.parse_wbc_match("日本", "中華台北")
    assert live_match is not None, "Crawler failed to find mock match"
    print("✅ Crawler Mock Data Fetching: OK")

    # 2. Test Integration in wbc_data/fetch_latest_wbc_match
    # We use live=True and use_mock=True for this environment
    match_data = fetch_latest_wbc_match(live=True, use_mock=True)
    
    # Verify TSL odds are present and match mock
    tsl_odds = [o for o in match_data.odds if o.book == "TSL"]
    assert len(tsl_odds) > 0, "Integrated TSL odds are missing"
    
    print(f"✅ Integrated TSL Odds Found: {len(tsl_odds)} lines")
    
    # Check for a specific value (e.g. ML Japan 1.42)
    jpn_ml = next((o for o in tsl_odds if o.market == "ML" and o.side == "JPN"), None)
    assert jpn_ml is not None, "JPN ML odds missing after integration"
    assert jpn_ml.price == 1.42, f"Price mismatch: expected 1.42, got {jpn_ml.price}"
    
    print(f"✅ Data Accuracy Check: JPN ML = {jpn_ml.price} (Correct)")
    
    print("\n=== Phase 1 Summary ===")
    print("TSL Crawler integrated successfully.")
    print("Automatic odds replacement verified.")
    print("System is ready for Phase 2: Feature Engineering.")

if __name__ == "__main__":
    test_phase_1()
