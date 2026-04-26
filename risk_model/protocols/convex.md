---
slug: convex
name: Convex Finance
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 1400000000
    since: 2021-05-17
dependencies:
  - id: curve
    type: dex_amm
    scope: [ethereum]
  - id: frax
    type: cdp_protocol
    scope: [ethereum]
    assets: [cvxFXS, FXS]
  - id: chainlink
    type: oracle_provider
    scope: [ethereum]
active_risks:
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "100% dependent on Curve incentive economics; Convex controls ~50% of veCRV vote — any change to CRV emission schedule or Curve governance directly undermines Convex model"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "cvxCRV/vlCVX governance — large vlCVX holders direct gauge vote allocation; hostile bribe market participant can redirect emissions away from key pools"
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "Entire Convex TVL model depends on CRV emissions remaining valuable; CRV price decline or emission reduction triggers reflexive TVL exit"
  - risk_id: whale_concentration
    deployment: ethereum
    note: "vlCVX (vote-locked CVX) is concentrated among large holders who dominate bribe market and gauge vote direction"
  - risk_id: lst_lrt_depeg
    deployment: ethereum
    note: "cvxCRV/CRV depeg risk: cvxCRV is not redeemable 1:1 for CRV; secondary market has traded at >10% discount during stress periods"
audits:
  - firm: PeckShield
    date: 2021-05
    url: ""
---

## Overview

Convex Finance is a yield booster for Curve liquidity providers, aggregating
veCRV voting power to maximize CRV rewards for depositors without requiring
them to lock CRV directly. Convex controls approximately 50% of all veCRV,
making it the dominant governance actor in the Curve ecosystem. CVX holders
lock as vlCVX to direct gauge votes, creating a bribe market (Votium). Total
TVL is approximately $1.4B, entirely dependent on Curve's continued CRV emissions.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Single-chain (Ethereum only). No cross-chain deployment divergence applicable.
Entire risk surface is concentrated in Ethereum and its Curve ecosystem.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value | Risk note |
|-----------|-------|-----------|
| veCRV controlled | ~50% of total | Dominant Curve governance actor |
| CRV lock type | cvxCRV (non-redeemable) | Secondary market depeg risk |
| vlCVX lock | 16-week lock | Illiquid governance position |
| Bribe market | Votium (~$5M+/epoch) | Vote-buying concentration risk |
| Frax exposure | cvxFXS position | FXS governance dependency |
