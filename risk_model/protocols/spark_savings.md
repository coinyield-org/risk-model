---
slug: spark_savings
name: Spark Savings (sDAI)
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 1800000000
    since: 2023-08-01
dependencies:
  - id: makerdao_sky
    type: governance
    scope: all_deployments
    note: "MakerDAO/Sky DAO sets the DAI Savings Rate (DSR); sDAI yield is entirely a governance parameter"
  - id: makerdao_dsr
    type: yield_source
    scope: [ethereum]
    note: "sDAI wraps the MakerDAO DAI Savings Rate contract; all yield flows through DSR"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "MakerDAO/Sky governance directly controls the DSR rate; a hostile or miscalibrated governance vote can set DSR to zero or near-zero, eliminating yield with no recourse for sDAI holders"
  - risk_id: downstream_protocol_failure
    deployment: ethereum
    note: "All sDAI value rests on MakerDAO's treasury allocation model; a systemic failure of MakerDAO (PSM insolvency, collateral shortfall) would directly impair sDAI backing at a 1:1 ratio"
  - risk_id: native_stablecoin_peg_stress
    deployment: ethereum
    note: "sDAI backing relies on DAI maintaining its peg; PSM imbalance or USDS migration friction can create redeem/withdraw mismatches"
audits: []
---

## Overview

Spark Savings (sDAI) is the yield-bearing wrapper for the MakerDAO DAI Savings Rate (DSR).
Users deposit DAI and receive sDAI, an ERC-4626 vault token that accrues interest as MakerDAO
allocates protocol revenue to the DSR. The contract is a minimal pass-through: no independent
risk logic, no isolated collateral — yield and backing are 100% determined by MakerDAO governance.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Single Ethereum deployment; no multi-chain surface. All risk is concentrated in the MakerDAO
mainnet governance and DSR smart contract stack.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Underlying | MakerDAO DAI Savings Rate (DSR) |
| Vault standard | ERC-4626 |
| Governance | MakerDAO/Sky DAO (executive vote) |
| Yield source | MakerDAO protocol surplus |
| Withdrawal delay | None (instant redeem against PSM) |
