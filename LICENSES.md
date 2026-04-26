# Licensing Map

This file explains how licensing applies across `coinyield-data`.

## 1. Content / curated model data

License: **CC BY-NC-SA 4.0**

Applies to repository-authored content such as:

- `risk_model/protocols/**`
- `risk_model/chains/**`
- `risk_model/types/**`
- `risk_model/taxonomy/**`
- `risk_model/incidents/**`
- `risk_model/attack_patterns/**`
- `risk_model/ARCHITECTURE.md`
- `risk_model/TODO.md`
- repository-authored Markdown docs in the repo root
- repository-authored `MANIFEST.md` files
- `risk_model/neo4j/generated/risk_model.cypher`

## 2. Tooling / scripts / infrastructure

License: **PolyForm Noncommercial 1.0.0**

Applies to repository-authored tooling such as:

- `**/*.py`
- `**/*.sh`
- `Makefile`
- `docker-compose.yml`
- `.github/workflows/**`
- hand-authored Neo4j helper files such as:
  - `risk_model/neo4j/checks.cypher`
  - `risk_model/neo4j/constraints.cypher`
  - `risk_model/neo4j/queries.cypher`
  - `risk_model/neo4j/load_generated.sh`
  - `risk_model/neo4j/ci_assert.sh`
  - `risk_model/neo4j/import_risk_model.py`

Required Notice:

- `Copyright (c) 2026 CoinYield`

## 3. Third-party materials

Excluded from the repository licenses unless a file explicitly says otherwise.

Examples:

- third-party audit PDFs
- externally authored security reports
- mirrored source documents

If a file was written by a third party, do not assume that the repository's
licenses apply to it.

## 4. Internal-only working files

Files under `internal/`, `audits/`, `dex_pools/`, and `postmortems/` are local
working inputs and are gitignored. They are not part of the intended public
repository surface.
