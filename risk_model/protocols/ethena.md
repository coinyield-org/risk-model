---
slug: ethena
name: Ethena USDe
types: [synthetic]
deployments:
  - chain: ethereum
    tvl_usd: 4800000000
    since: 2024-02-19
  - chain: arbitrum
    tvl_usd: 100000000
    since: 2024-05-01
  - chain: base
    tvl_usd: 100000000
    since: 2024-06-01
dependencies:
  - id: binance
    type: cex_venue
    scope: all_deployments
    note: "Primary venue for delta-neutral short perp hedges"
  - id: bybit
    type: cex_venue
    scope: all_deployments
    note: "Secondary perp hedge venue"
  - id: okx
    type: cex_venue
    scope: all_deployments
    note: "Secondary perp hedge venue"
  - id: copper
    type: custodian
    scope: all_deployments
    note: "Off-exchange custody (MPC) for collateral backing CEX positions"
  - id: ceffu
    type: custodian
    scope: all_deployments
    note: "Binance-affiliated off-exchange custodian for BTC/ETH collateral"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    assets: [ETH/USD, BTC/USD, stETH/ETH]
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    via: [sUSDe stakers as EigenLayer AVS backing]
active_risks:
  - risk_id: perp_funding_feedback
    deployment: [ethereum, arbitrum, base]
    note: "Ethena's delta hedge depends on positive perp funding rates; sustained negative funding (as occurred Mar 2023 and Aug 2023 on ETH perps) directly reduces USDe backing below par, creating a slow-bleed undercollateralization"
  - risk_id: rwa_issuer_default
    deployment: ethereum
    note: "Copper and Ceffu hold all spot collateral off-exchange; custodian insolvency or access freeze destroys delta-hedge backing without on-chain recourse"
  - risk_id: quoted_vs_underlying_depeg
    deployment: [ethereum, arbitrum, base]
    note: "sUSDe (staked USDe) can trade at a significant premium or discount to USDe during stress; forced liquidations of leveraged sUSDe positions amplify depeg"
  - risk_id: whale_coordination
    deployment: ethereum
    note: "Large-scale simultaneous redemptions drain the liquid reserve buffer faster than the protocol can unwind perp positions, creating transient undercollateralization"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "Basis price for the delta hedge is derived from CEX perp funding data, not a fully decentralized oracle; stale or manipulated funding rate data misprices the hedge"
audits:
  - firm: Cyfrin
    date: 2024-01
    url: ""
---

## Overview

Ethena issues USDe, a synthetic dollar backed by spot crypto (ETH, BTC, stETH) plus
an equal-notional short perp position on centralized exchanges (Binance, Bybit, OKX).
The delta-neutral book means USDe value is theoretically stable regardless of ETH/BTC price.
sUSDe is the staked form that accrues the net funding-rate yield earned on the short perp legs.
Collateral custody sits with Copper and Ceffu (off-exchange MPC custodians), not in smart contracts.

## Type-specific risks

See `types/synthetic.md` for base risk profile.

## Deployment divergence

Arbitrum and Base deployments hold bridged USDe/sUSDe with no independent hedge infrastructure;
all risk accrues on the Ethereum mainnet reserve backing. Cross-chain balances are exposed to
bridge dependency (canonical bridges) but carry no additional collateral risk surface beyond the mainnet model.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Collateral types | stETH, ETH, BTC, USDT (spot) |
| Hedge venues | Binance, Bybit, OKX (short perps) |
| Custodians | Copper, Ceffu |
| Reserve fund | ~$50M liquid buffer for negative funding periods |
| sUSDe unstaking delay | 7-day cooldown |
