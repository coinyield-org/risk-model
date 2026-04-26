---
slug: polymarket
name: Polymarket
types: []
deployments:
  - chain: polygon
    tvl_usd: 430000000
    since: 2020-06-01
dependencies:
  - id: uma_protocol
    type: oracle_provider
    scope: all_deployments
    note: optimistic oracle for market resolution
  - id: circle
    type: issuer
    scope: all_deployments
    assets: [USDC]
  - id: polymarket_team
    type: operator
    scope: all_deployments
    note: market creation and dispute resolution oversight
active_risks:
  - risk_id: fallback_oracle_misconfig
    note: "UMA optimistic oracle uses a challenge period; disputed resolutions can be contested but are subject to UMA governance, not on-chain finality"
  - risk_id: governance_hostile_decision
    note: "Polymarket team controls market creation and can influence resolution framing; no fully decentralized dispute layer"
  - risk_id: whale_coordination
    note: "Large position holders can move implied odds, creating reflexive incentives around market resolution outcomes"
audits:
  - firm: ChainSecurity
    date: 2021-01
    url: ""
---

## Overview

Polymarket is the largest decentralized prediction market, operating on Polygon with
~$0.43B in open interest (reported as TVL). Users trade binary outcome contracts
denominated in USDC. Market resolution relies on the UMA optimistic oracle with a
dispute window. In 2022 Polymarket settled with the CFTC for $1.4M over offering
unregistered event contracts to US users; US access is now restricted.

## Type-specific risks

Polymarket does not map to a standard DeFi type; base risk profile is specific to
prediction market mechanics: oracle resolution disputes, regulatory exposure, and
market-maker concentration.
