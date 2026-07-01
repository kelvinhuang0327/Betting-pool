# P212-A Open-Source MLB Dependency Decision Gate

Open-source MLB dependency decision gate only. Not live predictions, not betting advice.

## Decision

- Status: PASS_NEEDS_SEPARATE_OWNER_AUTHORIZATION
- Selected candidate: pybaseball
- Required notice: Dependency addition requires separate Owner authorization.
- This decision gate is not formal dependency adoption.
- No dependency files are modified by this gate.

## Candidate Matrix

| Candidate | Source / Package Reference | License | Maintenance / Release Signal | Python / Runtime Compatibility | Data Terms / MLB Notice Risk | Dependency Risk | Recommendation Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pybaseball | https://pypi.org/project/pybaseball/, https://github.com/jldbc/pybaseball | MIT license. | PyPI shows pybaseball 2.2.7 uploaded on 2023-09-08; the GitHub repository is public with issue/PR history visible as of 2026-07-01. | PyPI classifiers list Python 3.8, 3.9, 3.10, and 3.11. Local .venv import smoke found pybaseball 2.2.7 available on Python 3.13, but this task does not add or pin the dependency. | Medium: it wraps multiple public baseball data sites/APIs. Consumers must respect each upstream source's terms, rate limits, attribution, and cache expectations before production activation. | Requires a new Python dependency pin and transitive dependency review; no dependency file is changed by this gate. | SELECTED_FOR_SEPARATE_OWNER_AUTHORIZATION |
| MLB-StatsAPI | https://pypi.org/project/MLB-StatsAPI/, https://github.com/toddrob99/MLB-StatsAPI, https://gdx.mlb.com/components/copyright.txt | GPL-3.0 license. | PyPI shows version 1.9.0 released on 2025-04-04; GitHub repository is public and remains a recognized wrapper for statsapi-style team/schedule/player access as of 2026-07-01. | PyPI supports Python 3 and typical modern CPython usage; not currently installed in this repo's system python or .venv. | Medium: delegates to MLB Stats API/public MLB endpoints. MLB copyright and acceptable-use language must be reviewed before production use. | GPL-3.0 license creates a higher authorization burden for this repo. | REJECTED_FOR_INITIAL_DEPENDENCY_GATE_GPL_LICENSE_REVIEW_REQUIRED |
| python-mlb-statsapi | https://pypi.org/project/python-mlb-statsapi/, https://github.com/zero-sum-seattle/python-mlb-statsapi, https://gdx.mlb.com/components/copyright.txt | MIT license. | PyPI shows version 0.7.2 uploaded on 2026-02-05; GitHub repository is public and should still be reviewed before any dependency add. | PyPI requires Python >=3.10 and classifiers list Python 3.10 through 3.14; not currently installed in this repo's system python or .venv. | Medium: also relies on MLB Stats API/public MLB endpoints, so MLB terms, copyright, rate limits, and caching boundaries apply. | Python >=3.10 is compatible, but it is a secondary metadata client for this gate. | REJECTED_FOR_INITIAL_DEPENDENCY_GATE_SECONDARY_METADATA_CLIENT |
| baseballr | https://github.com/BillPetti/baseballr, https://cran.r-project.org/package=baseballr | MIT license. | CRAN/GitHub package is public and known in the baseball analytics ecosystem, but it introduces an R runtime dependency. | Not a Python library. Introducing R runtime is outside this task unless separately authorized by CTO/Owner. | Medium: wraps public baseball data sources with the same upstream terms and rate-limit concerns. | Requires an R runtime dependency that is outside this Python repo gate. | REJECTED_FOR_INITIAL_DEPENDENCY_GATE_R_RUNTIME_OUT_OF_SCOPE |

## Recommendation

Proceed only to a separate Owner authorization request for pybaseball as the initial open-source MLB dependency candidate for read-only historical/statcast data work.

Dependency addition requires separate Owner authorization.

Do not add pybaseball, MLB-StatsAPI, python-mlb-statsapi, baseballr, or any other MLB package in this gate.

## Required Authorizations

- Owner approval to modify dependency files in a separate task.
- Owner/legal acceptance of upstream public baseball data terms, rate limits, attribution, caching, and MLB notice boundaries before production use.
- CTO review before any production activation, DB write path, live provider call, or model integration.

## Rejected Candidates

- MLB-StatsAPI: REJECTED_FOR_INITIAL_DEPENDENCY_GATE_GPL_LICENSE_REVIEW_REQUIRED
- python-mlb-statsapi: REJECTED_FOR_INITIAL_DEPENDENCY_GATE_SECONDARY_METADATA_CLIENT
- baseballr: REJECTED_FOR_INITIAL_DEPENDENCY_GATE_R_RUNTIME_OUT_OF_SCOPE

## Dependency Files Detected

- requirements.txt

## Risk Boundaries

- No dependency addition.
- No dependency file mutation.
- No live or paid provider connection.
- No DB write.
- No production activation.
- No model logic change.

## Prohibited Claims

- future prediction
- betting advice
- production readiness
- edge
- ROI
- EV
- Kelly
- CLV

## Source Evidence

- P211-A Markdown: report/p211a_open_source_mlb_data_adoption.md
- P211-A JSON: report/p211a_open_source_mlb_data_adoption.json
- P211-A recommendation: Use pybaseball as the first optional read-only adapter for historical/statcast samples; consider MLB-StatsAPI later for team/schedule/player metadata after dependency and MLB terms authorization.

Open-source MLB dependency decision gate only. Not live predictions, not betting advice.
