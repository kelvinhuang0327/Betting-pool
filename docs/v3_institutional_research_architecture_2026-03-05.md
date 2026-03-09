# WBC V3 Institutional Research Architecture (2026-03-05)

## SECTION 1 — Full System Functional Audit

### 1.1 Data Flow Map
1. Data ingestion (`wbc_backend/ingestion/providers.py`)
2. Cleaning & validation (`wbc_backend/cleaning/preprocess.py`)
3. Advanced feature engineering (`wbc_backend/features/advanced.py`)
4. Ensemble prediction (`wbc_backend/models/ensemble.py`)
5. WBC rule adjustments (`wbc_backend/pipeline/wbc_rule_engine.py`)
6. Monte Carlo + market calibration (`wbc_backend/simulation/monte_carlo.py`, `wbc_backend/betting/market.py`)
7. Bet optimizer + risk controls (`wbc_backend/betting/optimizer.py`, `wbc_backend/betting/risk_control.py`)
8. Reporting (`wbc_backend/reporting/renderers.py`)

### 1.2 Structural Weaknesses
- Research/self-improve loop was not hard-gated by pass/fail phase validation.
- Pipeline fallback could continue with default matchup, masking data quality breaks.
- Backtesting harnesses were fragmented across scripts.

### 1.3 Modeling Blind Spots
- No residual alpha model on systematic forecast error.
- Regime classifier not deeply coupled to final uncertainty scaling.
- No adversarial validation gate against train/deploy distribution mismatch.

### 1.4 Missing Feature Domains
- Market microstructure features are not first-class in core model input.
- Psychological pressure proxies are not standardized in schema.
- Cross-market incoherence features (ML/RL/OU) not encoded as graph signals.

### 1.5 Data Leakage Risks
- Potential odds timestamp leakage if close-adjacent quotes enter pregame training snapshot.
- Single adjusted probability reused in downstream path without nested calibration decomposition.

### 1.6 Regime Dependency Risks
- Pool vs knockout transition risk not fully parameterized end-to-end.
- Liquidity regime not directly linked to allowed position sizing in base risk module.

### 1.7 Correlation Risks
- Heuristic portfolio allocation without scenario covariance estimation.
- Venue/weather cluster concentration not formally constrained.

### 1.8 Stability Weaknesses (Fixed)
- `compute_clutch_index` had missing return path.
- `ensemble` path had optional field assumptions and uninitialized diagnostics risk.

## SECTION 2 — Feature Space Expansion

Implemented in `wbc_backend/research/feature_space.py`:
- Team strength features
- Pitcher micro-metrics
- Bullpen fatigue metrics
- Lineup synergy metrics
- Game theory variables
- Travel & rest factors
- Weather variables
- Market microstructure signals
- Line movement velocity
- Sharp money detection
- Closing line divergence
- Volatility clustering
- Cross-market correlation
- Score state transition probabilities
- Psychological pressure proxies

Per domain, the framework defines:
- Feature definition
- Signal hypothesis
- Quantification method
- Data requirements
- Validation protocol

## SECTION 3 — Methodological Expansion

Implemented in `wbc_backend/research/methodology.py`:
- Dynamic ensemble weighting
- Online learning
- Bayesian updating
- Regime-switching models
- Hidden Markov Models
- Hierarchical Bayesian models
- Survival analysis
- Reinforcement learning
- Meta-labeling
- Residual modeling
- Model stacking with meta learner
- Adversarial validation
- Feature stability selection
- Cross-season generalization testing

Implementation utilities included:
- `dynamic_ensemble_weights()`
- `bayesian_beta_update()`

## SECTION 4 — Risk & Portfolio Optimization Upgrade

Implemented in `wbc_backend/research/portfolio_v3.py`:
- Correlation-adjusted Kelly
- Covariance estimation (PSD-repaired)
- CVaR optimization
- Stress scenario simulation
- Drawdown-adaptive sizing
- Bankroll survival probability modeling

Core formulas:
- Kelly proxy: `w* ~ Sigma^{-1} * mu`
- Portfolio loss: `L = -(R @ w)`
- `CVaR_alpha = E[L | L >= VaR_alpha]`
- Objective: `score = E[R_p] - lambda * CVaR`

## SECTION 5 — Research Infrastructure Design

Implemented in `wbc_backend/research/infrastructure.py`:
- Walk-forward validation windows
- Cross-year validation splits
- Monte Carlo season simulation
- Hyperparameter search protocol
- Feature ablation testing
- Edge decay half-life analysis
- CLV tracking engine
- Calibration monitoring (`Brier`, `logloss`, `ECE`, `MCE`)
- Drift detection (`PSI` + empirical `KS`)

## SECTION 6 — Implementation Phase Plan

Implemented in `wbc_backend/research/phase_plan.py`:
- Phase 1: Functional audit + stability hardening
- Phase 2: Feature-space expansion protocol
- Phase 3: Methodological expansion
- Phase 4: Portfolio/risk upgrade
- Phase 5: Continuous research infrastructure
- Phase 6: End-to-end phase executor

Each phase includes:
- Objectives
- Files
- Algorithms
- Pseudocode
- Testing strategy
- Validation metrics

## SECTION 7 — Execute Implementation (Completed)

### Phase-by-phase execution engine
Implemented in `wbc_backend/research/execution.py` (`V3ResearchExecutor`):
1. Execute phase
2. Validate pass/fail criteria
3. Stop immediately on failure
4. Continue only when phase passes

### Tests implemented
- `tests/test_model_stability_fixes.py`
- `tests/test_v3_research_architecture.py`
- `tests/test_runtime_and_optimizer_regression.py`

### Test run result
- Command: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Result: `Ran 57 tests ... OK`

### Phase gate result
- Phase 1: PASS
- Phase 2: PASS
- Phase 3: PASS
- Phase 4: PASS
- Phase 5: PASS
- Phase 6: PASS

## Deliverable Summary

V3 architecture now provides a self-improving research backbone with deterministic phase gates, exhaustive feature/method catalogs, covariance-aware portfolio controls, and continuous calibration/CLV/drift monitoring.
It is now deployable in operations through:
- CLI entry `--research-cycle` (`wbc_backend/run.py`)
- scheduler task `research_cycle` (`wbc_backend/scheduler/jobs.py`)
- persisted artifact output (`wbc_backend/research/runtime.py`, `data/wbc_backend/artifacts/v3_research_cycle.json`)
