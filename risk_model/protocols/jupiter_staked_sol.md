---
slug: jupiter_staked_sol
name: Jupiter Staked SOL (JupSOL)
types: [lst]
deployments:
  - chain: solana
    tvl_usd: 840000000
    since: 2024-01-01
dependencies:
  - id: solana_validators
    type: infrastructure
    scope: all_deployments
  - id: pyth_network
    type: oracle_provider
    scope: all_deployments
    assets: [JupSOL]
  - id: solana_foundation_stake_program
    type: staking_protocol
    scope: all_deployments
active_risks:
  - risk_id: chain_halt
    deployment: solana
    note: "Solana network halts prevent unstaking, liquidations of JupSOL-collateralized positions, and exchange rate updates"
  - risk_id: withdrawal_queue_delay
    deployment: solana
    note: "Solana uses epoch-based unstaking (~2–3 day delay per epoch); instant liquidity depends entirely on secondary market depth"
  - risk_id: quoted_vs_underlying_depeg
    deployment: solana
    note: "JupSOL market price can diverge from the on-chain exchange rate to SOL during stress or thin liquidity periods"
audits: []
---

## Overview

Jupiter Staked SOL (JupSOL) is a liquid staking token on Solana. Users deposit SOL into Jupiter's stake pool; the pool delegates to a curated set of validators selected by the Jupiter team. JupSOL accrues staking rewards and is redeemable for SOL subject to Solana's epoch-based unstaking schedule.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Solana LST mechanics differ substantially from Ethereum LSTs:
- Unstaking is epoch-gated (~2–3 days); there is no instant redemption path other than secondary market swaps
- Validator selection is controlled by Jupiter — operator concentration risk is higher than permissionless stake pools
- Solana outages affect both exchange rate oracle updates (Pyth) and the ability to trade JupSOL on-chain simultaneously

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Validator selection | Jupiter team discretion |
| Unstaking delay | ~2–3 days (epoch-based) |
| Exchange rate oracle | Pyth JupSOL/SOL |
| Underlying stake program | Solana Foundation stake pool program |
