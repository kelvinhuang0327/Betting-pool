# P211-A Open-Source MLB Data Library Adoption Spike

Historical/read-only MLB data adoption spike only. Not live predictions, not betting advice.

## Scope

- Read-only adoption spike only.
- No DB writes, no paid provider calls, no live odds calls, no production activation.
- No dependency files were modified; optional imports only.

## Candidate Evaluation

| Package | Purpose | License | Maintenance / Release Evidence | Python Compatibility | Data Terms Risk | Fit | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pybaseball | Python package for historical baseball data including Statcast, FanGraphs, Baseball Reference, and player/team lookup helpers. | MIT license. | PyPI shows pybaseball 2.2.7 uploaded on 2023-09-08; the GitHub repository is public with issue/PR history visible as of 2026-07-01. | PyPI classifiers list Python 3.8, 3.9, 3.10, and 3.11. Local .venv import smoke found pybaseball 2.2.7 available on Python 3.13, but this task does not add or pin the dependency. | Medium: it wraps multiple public baseball data sites/APIs. Consumers must respect each upstream source's terms, rate limits, attribution, and cache expectations before production activation. | Best fit for historical/statcast adoption spike because it covers the requested statcast/historical surface without custom MLB scraping logic. | RECOMMENDED_FOR_READ_ONLY_SPIKE_WITH_OPTIONAL_IMPORT |
| MLB-StatsAPI | Python wrapper for MLB Stats API endpoints covering teams, schedule, players, standings, and game metadata. | GPL-3.0 license. | PyPI shows version 1.9.0 released on 2025-04-04; GitHub repository is public and remains a recognized wrapper for statsapi-style team/schedule/player access as of 2026-07-01. | PyPI supports Python 3 and typical modern CPython usage; not currently installed in this repo's system python or .venv. | Medium: delegates to MLB Stats API/public MLB endpoints. MLB copyright and acceptable-use language must be reviewed before production use. | Functionally useful for read-only team, schedule, and player metadata, but GPL-3.0 licensing requires Owner/license review before dependency add. | CANDIDATE_REQUIRES_LICENSE_REVIEW_BEFORE_AUTHORIZATION |
| python-mlb-statsapi | Object-oriented Python client around MLB Stats API data models for teams, players, games, stats, and related metadata. | MIT license. | PyPI shows version 0.7.2 uploaded on 2026-02-05; GitHub repository is public and should still be reviewed before any dependency add. | PyPI requires Python >=3.10 and classifiers list Python 3.10 through 3.14; not currently installed in this repo's system python or .venv. | Medium: also relies on MLB Stats API/public MLB endpoints, so MLB terms, copyright, rate limits, and caching boundaries apply. | Possible object-oriented alternative for normalized team/player metadata, but not preferred over pybaseball plus MLB-StatsAPI for this spike. | SECONDARY_CANDIDATE_NOT_ADOPTED_IN_SPIKE |
| baseballr | R package for baseball data retrieval and analysis across MLB public sources. | MIT license. | CRAN/GitHub package is public and known in the baseball analytics ecosystem, but it introduces an R runtime dependency. | Not a Python library. Introducing R runtime is outside this task unless separately authorized by CTO/Owner. | Medium: wraps public baseball data sources with the same upstream terms and rate-limit concerns. | Useful comparison point only. Not suitable for this Python repo spike without explicit runtime authorization. | NOT_ADOPTED_R_RUNTIME_REQUIRES_SEPARATE_AUTHORIZATION |

## Adapter Diagnostics

| Provider | Package | Import | Installed | Importable | Version | Status | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mlb_statsapi | MLB-StatsAPI | statsapi | False | False |  | SKIPPED_MISSING_OPTIONAL_DEPENDENCY | Optional dependency 'MLB-StatsAPI' is not installed. This spike does not modify dependency files; add it only after Owner authorization. |
| pybaseball | pybaseball | pybaseball | False | False |  | SKIPPED_MISSING_OPTIONAL_DEPENDENCY | Optional dependency 'pybaseball' is not installed. This spike does not modify dependency files; add it only after Owner authorization. |
| python_mlb_statsapi | python-mlb-statsapi | mlbstatsapi | False | False |  | SKIPPED_MISSING_OPTIONAL_DEPENDENCY | Optional dependency 'python-mlb-statsapi' is not installed. This spike does not modify dependency files; add it only after Owner authorization. |

## Recommendation

Use pybaseball as the first optional read-only adapter for historical/statcast samples; consider MLB-StatsAPI later for team/schedule/player metadata after dependency and MLB terms authorization.

## Evidence URLs

- pybaseball: https://pypi.org/project/pybaseball/
- pybaseball: https://github.com/jldbc/pybaseball
- MLB-StatsAPI: https://pypi.org/project/MLB-StatsAPI/
- MLB-StatsAPI: https://github.com/toddrob99/MLB-StatsAPI
- MLB-StatsAPI: https://gdx.mlb.com/components/copyright.txt
- python-mlb-statsapi: https://pypi.org/project/python-mlb-statsapi/
- python-mlb-statsapi: https://github.com/zero-sum-seattle/python-mlb-statsapi
- python-mlb-statsapi: https://gdx.mlb.com/components/copyright.txt
- baseballr: https://github.com/BillPetti/baseballr
- baseballr: https://cran.r-project.org/package=baseballr

## Validation Notes

- Adapter fetch methods raise AdapterUnavailableError with clear reasons when packages are missing.
- Audit script performs deterministic diagnostics only and does not call live MLB endpoints.
- All output is labeled historical/read-only and excludes wagering-performance or staking claims.

Historical/read-only MLB data adoption spike only. Not live predictions, not betting advice.
