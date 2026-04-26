---
slug: jupiter_lend
name: Jupiter Lend
types: [lending]
deployments:
  - chain: solana
    tvl_usd: 880000000
    since: 2024-01-01
dependencies:
  - id: pyth_network
    type: oracle_provider
    scope: all_deployments
  - id: solana_validators
    type: infrastructure
    scope: all_deployments
  - id: jupiter_exchange
    type: parent_protocol
    scope: all_deployments
active_risks:
  - risk_id: oracle_staleness
    deployment: solana
    note: "Solana outages directly interrupt Pyth price updates — stale prices served during chain downtime"
  - risk_id: chain_halt
    deployment: solana
    note: "Solana has a documented history of full network outages; lending positions cannot be liquidated during halts"
  - risk_id: single_keeper_dependency
    deployment: solana
    note: "Liquidation architecture on Solana differs from EVM — keeper infrastructure is less mature and more concentrated"
audits: []
---

## Overview

Jupiter Lend is a lending protocol on Solana, built under the Jupiter Exchange ecosystem. Users supply assets as collateral and borrow against them under an overcollateralized model. Liquidation and interest mechanics follow standard lending design adapted for Solana's account model and transaction structure.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Solana-specific surface materially differs from EVM lending:
- No mempool — liquidation bots operate via different scheduling mechanisms; keeper infrastructure is less battle-tested than on Ethereum
- Solana outages (multiple documented in 2022–2023) halt all on-chain activity including liquidations; Pyth feeds go stale simultaneously
- Transaction throughput and fee model differ from EVM — gas-war liquidation dynamics do not apply, but congestion during stress events can delay keeper tx inclusion

## Key parameters

| Asset | Notes |
|-------|-------|
| SOL | Primary collateral; oracle via Pyth SOL/USD |
| USDC | Primary borrow asset |
| JupSOL | Accepted collateral; LST depeg surface |
