
# P102 Outcome-Only Strategy Backtest Scorecard — 2026-05-31

## Final Classification
P102_OUTCOME_ONLY_SCORECARD_READY_DIAGNOSTIC_ONLY

## Scorecard Summary
{
  "ALL_ROWS": {
    "n": 808,
    "hit_rate": 0.5693069306930693,
    "auc": 0.5246626686656672,
    "brier": 0.2661819269403243,
    "ece": 0.11423626732673269,
    "monthly_hit_rate": {
      "2026-05": 0.5895953757225434,
      "2026-04": 0.5424164524421594,
      "2026-03": 0.6164383561643836
    },
    "side_hit_rate": {
      "home": 0.5922330097087378,
      "away": 0.5454545454545454
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "HIGH_FIP": {
    "n": 133,
    "hit_rate": 0.6240601503759399,
    "auc": 0.5,
    "brier": 0.33962406015037583,
    "ece": 0.3240601503759398,
    "monthly_hit_rate": {
      "2026-05": 0.6363636363636364,
      "2026-04": 0.6229508196721312,
      "2026-03": 0.5882352941176471
    },
    "side_hit_rate": {
      "away": 0.6240601503759399
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "diagnostic_only"
  },
  "MID_FIP": {
    "n": 343,
    "hit_rate": 0.5306122448979592,
    "auc": 0.5277114190157668,
    "brier": 0.2617660488930758,
    "ece": 0.10088284839650147,
    "monthly_hit_rate": {
      "2026-05": 0.5510204081632653,
      "2026-04": 0.5176470588235295,
      "2026-03": 0.5
    },
    "side_hit_rate": {
      "away": 0.49142857142857144,
      "home": 0.5714285714285714
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "LOW_FIP": {
    "n": 178,
    "hit_rate": 0.5280898876404494,
    "auc": 0.48467578520770016,
    "brier": 0.2531418100980731,
    "ece": 0.043820713483145986,
    "monthly_hit_rate": {
      "2026-05": 0.5617977528089888,
      "2026-04": 0.4868421052631579,
      "2026-03": 0.5384615384615384
    },
    "side_hit_rate": {
      "home": 0.5222222222222223,
      "away": 0.5340909090909091
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "PRIMARY_125": {
    "n": 491,
    "hit_rate": 0.6028513238289206,
    "auc": 0.5175502425502426,
    "brier": 0.26966776292653355,
    "ece": 0.1349669490835031,
    "monthly_hit_rate": {
      "2026-05": 0.6091370558375635,
      "2026-04": 0.5867768595041323,
      "2026-03": 0.6538461538461539
    },
    "side_hit_rate": {
      "home": 0.6118012422360248,
      "away": 0.5857988165680473
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "SHADOW_100": {
    "n": 536,
    "hit_rate": 0.5951492537313433,
    "auc": 0.5211418170261329,
    "brier": 0.27053091182355593,
    "ece": 0.13818938432835826,
    "monthly_hit_rate": {
      "2026-05": 0.6164383561643836,
      "2026-04": 0.5708812260536399,
      "2026-03": 0.625
    },
    "side_hit_rate": {
      "home": 0.6118012422360248,
      "away": 0.5700934579439252
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "TIER_A": {
    "n": 84,
    "hit_rate": 0.4880952380952381,
    "auc": 0.4736245036868973,
    "brier": 0.2512305411859881,
    "ece": 0.016630416666666665,
    "monthly_hit_rate": {
      "2026-05": 0.5652173913043478,
      "2026-04": 0.38235294117647056,
      "2026-03": 0.5
    },
    "side_hit_rate": {
      "home": 0.4878048780487805,
      "away": 0.4883720930232558
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  },
  "TIER_B": {
    "n": 94,
    "hit_rate": 0.5638297872340425,
    "auc": 0.48412333179935574,
    "brier": 0.25484975253014897,
    "ece": 0.06811842553191487,
    "monthly_hit_rate": {
      "2026-05": 0.5581395348837209,
      "2026-04": 0.5714285714285714,
      "2026-03": 0.5555555555555556
    },
    "side_hit_rate": {
      "home": 0.5510204081632653,
      "away": 0.5777777777777777
    },
    "rolling_stability": 0.0,
    "sample_limitation": false,
    "diagnostic_status": "watch_only"
  }
}

## Strongest Diagnostic Signal
HIGH_FIP

## Watch-Only Signals
['MID_FIP', 'LOW_FIP']

## Learning Recommendation
{
  "track_next": [
    "ALL_ROWS",
    "HIGH_FIP",
    "MID_FIP",
    "LOW_FIP",
    "PRIMARY_125",
    "SHADOW_100",
    "TIER_A",
    "TIER_B"
  ],
  "do_not_promote": [
    "ALL_ROWS",
    "MID_FIP",
    "LOW_FIP",
    "PRIMARY_125",
    "SHADOW_100",
    "TIER_A",
    "TIER_B"
  ],
  "needs_more_data": [],
  "compare_when_coverage_increases": []
}

## Governance
- paper_only=true
- diagnostic_only=true
- production_ready=false
- recommendation_allowed=false
- odds_used=false
- ev_computed=false
- clv_computed=false
- kelly_computed=false
- stake_sizing=false
