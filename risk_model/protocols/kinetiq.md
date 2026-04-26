---
slug: kinetiq
name: Kinetiq kHYPE
types: [lst]
deployments:
  - chain: hyperliquid_l1
    tvl_usd: 770000000
    since: 2024-01-01
dependencies:
  - id: hyperliquid_validators
    type: infrastructure
    scope: all_deployments
  - id: kinetiq_team
    type: governance
    scope: all_deployments
active_risks:
  - risk_id: chain_halt
    deployment: hyperliquid_l1
    note: "Hyperliquid L1 is a new chain with limited track record; consensus failure or network halt would freeze all kHYPE operations"
  - risk_id: quoted_vs_underlying_depeg
    deployment: hyperliquid_l1
    note: "kHYPE market price may diverge from HYPE exchange rate; thin secondary liquidity on a new chain amplifies depeg persistence"
  - risk_id: governance_signer_key_leak
    deployment: hyperliquid_l1
    note: "Kinetiq is early-stage with centralized governance; multisig key compromise enables unauthorized protocol changes"
  - risk_id: whale_coordination
    deployment: hyperliquid_l1
    note: "Small validator set and concentrated token distribution increase the impact of coordinated whale withdrawal or governance pressure"
audits:
  - firm: Spearbit
    date: 2024-01
    url: ""
  - firm: Spearbit
    date: 2024-06
    url: ""
---

## Overview

Kinetiq kHYPE is a liquid staking token on Hyperliquid L1. Users deposit HYPE; the protocol delegates to the Hyperliquid validator set and issues kHYPE representing a staked HYPE claim plus accrued rewards. Kinetiq is an early-stage protocol on a new chain with a small validator set and centralized governance by the Kinetiq team.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

No multi-chain deployment. All operations are on Hyperliquid L1, which introduces chain-specific surface:
- Hyperliquid's validator set is small relative to Ethereum — operator concentration is structurally higher
- The chain has a limited production history; consensus failure scenarios are less well-characterized than on Ethereum or Solana
- Secondary market liquidity for kHYPE is nascent, limiting arbitrage capacity to close exchange rate deviations

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Validator set | Hyperliquid L1 validators (small set) |
| Operator selection | Kinetiq team discretion |
| Upgrade authority | Kinetiq multisig (early-stage) |
| Audits | 2 Spearbit reports |
