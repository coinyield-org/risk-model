---
slug: etherfi
name: ether.fi
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 5300000000
    since: 2024-02-15
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-04-01
    note: "eETH bridged via LayerZero OFT; no native restaking on Arbitrum"
  - chain: base
    tvl_usd: 0
    since: 2024-04-01
    note: "eETH bridged via LayerZero OFT; no native restaking on Base"
dependencies:
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    note: "All restaked ETH is delegated to EigenLayer; AVS slashing conditions apply"
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
    note: "Native ETH validators underpinning eETH"
  - id: etherfi_operators
    type: node_operator_set
    scope: [ethereum]
    note: "ether.fi curates its own operator set for node operations; not fully permissionless"
  - id: chainlink
    type: oracle_provider
    scope: [ethereum]
    assets: [eETH/ETH exchange rate]
  - id: layerzero
    type: bridge
    scope: [arbitrum, base]
    assets: [eETH (weETH OFT)]
    note: "Cross-chain eETH (weETH) uses LayerZero OFT standard"
active_risks:
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "ether.fi operators are delegated into EigenLayer AVSs; novel AVS slashing conditions (live 2024-2025) could reduce eETH backing if an AVS misbehavior event triggers a large slash — risk is compounded by the still-maturing nature of AVS slashing parameters"
  - risk_id: operator_concentration
    deployment: ethereum
    note: "ether.fi curates its operator set rather than using a fully permissionless marketplace; a small set of operators handle the majority of ether.fi-delegated stake, creating correlated infrastructure risk"
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "eETH redemption requires both EigenLayer's 7-day unstaking delay and Ethereum's beacon-chain exit queue; combined wait can exceed 2 weeks under high exit demand, sustaining exchange rate dislocations"
  - risk_id: bridge_dep
    deployment: [arbitrum, base]
    note: "Cross-chain weETH relies on LayerZero OFT; a LayerZero exploit or pause would orphan weETH on L2s from its Ethereum backing"
  - risk_id: exchange_rate_vs_market_depeg
    deployment: [ethereum, arbitrum, base]
    note: "eETH/weETH market price can deviate from its ETH exchange rate during AVS slashing events or withdrawal queue saturation; L2 bridged versions lag any on-chain exchange rate update by LayerZero message latency"
audits:
  - firm: Certora
    date: 2024-01
    url: ""
  - firm: Trail of Bits
    date: 2024-02
    url: ""
  - firm: Sigma Prime
    date: 2024-03
    url: ""
  - firm: OpenZeppelin
    date: 2024-04
    url: ""
  - firm: Sherlock
    date: 2024-05
    url: ""
---

## Overview

ether.fi is the largest liquid restaking protocol by TVL, issuing eETH (rebasing)
and weETH (wrapped, exchange-rate-accruing) backed by natively staked ETH delegated
into EigenLayer. Unlike some LRTs, ether.fi operates its own node infrastructure
and curates the operator set that runs its validators. weETH is bridged to Arbitrum
and Base via LayerZero OFT, making it a widely used LRT collateral across L2 DeFi.
The protocol is exposed to both Ethereum consensus-layer risk and EigenLayer AVS
slashing risk simultaneously.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Arbitrum and Base deployments are bridged weETH (LayerZero OFT) — not natively
restaked on those chains. This means:
- Exchange rate updates must be messaged cross-chain; stale rate risk during L1 congestion.
- LayerZero bridge failure or pause strands weETH on L2 without redemption path.
- Aave, Morpho, and other L2 protocols that accept weETH as collateral inherit this
  bridge dependency transitively.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Underlying staking layer | EigenLayer (native ETH restaking) |
| Operator model | Curated set (ether.fi-managed) |
| Withdrawal delay | EigenLayer 7-day + beacon exit queue |
| Cross-chain bridge | LayerZero OFT (weETH) |
| Oracle (exchange rate) | Chainlink eETH/ETH |
| Protocol fee | ~10% of staking + restaking rewards |
