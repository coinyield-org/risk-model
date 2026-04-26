---
slug: avalon_usda
name: Avalon USDa
types: [cdp]
deployments:
  - chain: bnb
    tvl_usd: 410000000
    since: 2024-01-01
  - chain: ethereum
    tvl_usd: 0
    since: 2024-06-01
  - chain: merlin_chain
    tvl_usd: 0
    since: 2024-06-01
dependencies:
  - id: btc_collateral
    type: collateral_asset
    scope: all_deployments
    assets: [WBTC, FBTC]
  - id: avalon_team
    type: governance
    scope: all_deployments
  - id: bnb_validators
    type: underlying_chain
    scope: [bnb]
active_risks:
  - risk_id: fallback_oracle_misconfig
    note: "BTC DeFi oracle infrastructure on BNB Chain and Merlin Chain is less mature than Ethereum; coverage gaps and stale feeds are credible risks"
  - risk_id: ltv_too_aggressive
    note: "BTC price volatility can erode collateralization buffers rapidly; USDa peg depends on timely liquidations"
  - risk_id: governance_hostile_decision
    note: "Avalon team controls risk parameters (LTV, liquidation thresholds, collateral types) without a mature DAO structure"
  - risk_id: deployer_key_leak
    note: "Protocol is early-stage with centralized upgrade authority; key compromise allows arbitrary parameter or logic changes"
audits: []
---

## Overview

Avalon USDa is a BTC-collateralized CDP protocol operating primarily on BNB Chain,
with additional deployments on Ethereum and Merlin Chain. Users deposit WBTC or
FBTC to mint USDa, a USD-pegged stablecoin. The protocol is designed for the
emerging BTC DeFi ecosystem and carries the oracle and liquidation risks inherent
in collateralizing with a single volatile asset (BTC) on chains with less mature
DeFi infrastructure than Ethereum.

## Type-specific risks

See `types/cdp.md` for base risk profile.

## Deployment divergence

BNB Chain is the primary deployment. Merlin Chain deployment adds further risk:
Merlin is a new BTC L2 with limited oracle infrastructure and a centralized sequencer.
Per-chain oracle providers and liquidation keepers differ across deployments.

## Key parameters

| Chain | Collateral | Notes |
|-------|-----------|-------|
| bnb | WBTC, FBTC | Chainlink BTC/USD (BNB chain feed) |
| merlin_chain | FBTC | Oracle coverage limited on BTC L2 |
| ethereum | WBTC | More mature oracle infrastructure |
