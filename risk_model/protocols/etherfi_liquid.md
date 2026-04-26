---
slug: etherfi_liquid
name: ether.fi Liquid
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 450000000
    since: 2024-01-01
dependencies:
  - id: etherfi
    type: staking_protocol
    scope: all_deployments
    assets: [eETH, weETH]
  - id: morpho
    type: lending_protocol
    scope: all_deployments
    note: allocation target
  - id: pendle
    type: yield_trading
    scope: all_deployments
    note: PT allocation target
  - id: eigenlayer
    type: restaking_protocol
    scope: all_deployments
    via: [etherfi]
active_risks:
  - risk_id: downstream_protocol_failure
    note: "Concentrated allocation across ether.fi ecosystem — stress in etherfi/Morpho/Pendle propagates directly to Liquid vault"
  - risk_id: deep_chain_yield_trading
    note: "Pendle PT positions create a 4-layer dependency: Liquid → Pendle PT → underlying yield source → EigenLayer AVSs"
  - risk_id: incentive_end_liquidity_flight
    note: "Significant mercenary TVL attracted by ether.fi loyalty points; emission reduction or program end risks rapid outflow"
  - risk_id: lst_lrt_depeg
    note: "weETH market price vs exchange rate divergence flows through to Liquid NAV"
audits: []
---

## Overview

ether.fi Liquid is an onchain capital allocator that routes user deposits across the
ether.fi ecosystem and selected DeFi protocols — primarily Morpho vaults and Pendle
PT positions — to optimize yield. TVL (~$0.45B) is closely coupled to the broader
ether.fi product suite. Audits are covered under the ether.fi core protocol (see
`09_etherfi`); no separate Liquid-specific PDFs are indexed.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Single Ethereum deployment; no cross-chain complexity.
