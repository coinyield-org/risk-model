---
slug: compound_v3
name: Compound V3
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 1000000000
    since: 2022-08-26
  - chain: arbitrum
    tvl_usd: 200000000
    since: 2023-06-01
  - chain: base
    tvl_usd: 100000000
    since: 2023-08-09
  - chain: polygon
    tvl_usd: 60000000
    since: 2023-05-01
  - chain: optimism
    tvl_usd: 40000000
    since: 2023-11-01
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: "Primary price feed for all collateral assets across all deployments"
  - id: openzeppelin_governor
    type: governance_framework
    scope: all_deployments
    note: "Compound uses OpenZeppelin Governor for on-chain governance with COMP token voting"
  - id: comp_token
    type: governance_token
    scope: all_deployments
    note: "COMP token voting weight determines all governance outcomes; historically concentrated among early investors and the Compound Labs team"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: all
    note: "COMP governance has historically responded slowly to risk events (e.g., slow reaction to collateral de-listings and parameter adjustments during market stress in 2022-2023); COMP voting power is concentrated among early investors and delegates, enabling low-turnout capture of risk parameter decisions"
  - risk_id: oracle_staleness
    deployment: [arbitrum, base, optimism, polygon]
    note: "Chainlink feeds on L2 deployments depend on sequencer liveness; Compound V3 does not uniformly enforce sequencer uptime checks, creating windows on L2 where stale prices are consumed during sequencer downtime"
  - risk_id: whale_coordination
    deployment: ethereum
    note: "COMP voting power is concentrated among a small number of large delegates; a coordinated governance capture could modify risk parameters (LTVs, supply caps, collateral listings) with limited checks from the broader token holder base"
  - risk_id: liquidation_bonus_too_small
    deployment: all
    note: "Compound V3 introduced a lower liquidation incentive model versus V2 to improve borrower experience; this reduces liquidator profitability on volatile assets during rapid price drops, risking delayed liquidations and bad debt accumulation when gas costs are elevated"
audits:
  - firm: Trail of Bits
    date: 2022-06
    url: ""
  - firm: Trail of Bits
    date: 2022-12
    url: ""
  - firm: Halborn
    date: 2023-04
    url: ""
---

## Overview

Compound V3 (Comet) restructured Compound's lending model around single-asset base markets:
each deployment supports one borrowable asset (e.g., USDC, ETH) and a set of approved collateral
types. This concentrates liquidity and simplifies risk isolation but removes cross-collateral
flexibility. COMP governance controls all market parameters across all deployments. The protocol
has a strong multi-year track record but has historically been slow to adapt risk parameters to
changing market conditions.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Ethereum mainnet carries the largest TVL and hosts the governance contracts. L2 deployments
(Arbitrum, Base, Polygon, Optimism) inherit sequencer dependency risk for oracle freshness;
Compound V3 does not consistently enforce sequencer uptime feed checks across all L2 markets,
creating asymmetric staleness exposure vs the mainnet deployment.

## Key parameters (ethereum USDC market, as of 2026-01)

| Asset | Collateral factor | Liquidation factor | Oracle |
|-------|------------------|--------------------|--------|
| ETH | 83% | 90% | Chainlink ETH/USD |
| wstETH | 82% | 90% | Chainlink wstETH/ETH + ETH/USD |
| WBTC | 80% | 85% | Chainlink BTC/USD |
| cbBTC | 80% | 85% | Chainlink BTC/USD |
