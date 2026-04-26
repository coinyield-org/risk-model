---
slug: jupiter_perps
name: Jupiter Perpetual Exchange
types: [perps]
deployments:
  - chain: solana
    tvl_usd: 700000000
    since: 2024-01-01
dependencies:
  - id: pyth_network
    type: oracle_provider
    scope: all_deployments
  - id: jlp_pool
    type: liquidity_pool
    scope: all_deployments
  - id: solana_validators
    type: infrastructure
    scope: all_deployments
active_risks:
  - risk_id: oracle_staleness
    deployment: solana
    note: "Pyth mark price feeds go stale during Solana outages — positions cannot be fairly settled or liquidated during downtime"
  - risk_id: chain_halt
    deployment: solana
    note: "Solana outages halt all protocol operations; liquidations, settlements, and funding payments are suspended for the outage duration"
  - risk_id: quoted_vs_underlying_depeg
    deployment: solana
    note: "JLP pool price and mark price can diverge during oracle lag — exploitable spread between mark price and fair value"
audits: []
---

## Overview

Jupiter Perpetual Exchange is a Solana-based derivatives protocol offering perpetual futures. Liquidity is provided by the JLP (Jupiter Liquidity Pool), whose holders act as the counterparty to all trader positions. Mark prices are sourced from Pyth Network. The protocol's risk profile is tightly coupled to Solana's liveness and Pyth feed reliability.

## Type-specific risks

See `types/perps.md` for base risk profile.

## Deployment divergence

No multi-chain deployment. Solana-specific surface dominates:
- JLP holders bear the aggregate PnL of all trader positions; sustained directional skew (more longs than shorts in a bull market) transfers wealth from JLP to traders — lp_pool_pnl_risk is structural, not incidental
- Pyth oracle outages coincide with Solana network outages, meaning mark price feeds fail exactly when volatility is highest and liquidation need is greatest
- Solana's lack of a public mempool changes frontrunning and liquidation dynamics relative to EVM perps; keeper infrastructure is less commoditized

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Mark price oracle | Pyth Network |
| Liquidity pool | JLP (LPs are counterparty to all positions) |
| Funding mechanism | Periodic funding payments between longs and shorts |
| Insurance fund | Jupiter-managed; runway not publicly disclosed |
