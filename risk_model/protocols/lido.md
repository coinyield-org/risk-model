---
slug: lido
name: Lido
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 22000000000
    since: 2020-12-18
  - chain: arbitrum
    tvl_usd: 0
    since: 2022-09-01
    note: "wstETH bridged only — no native staking deployment"
  - chain: optimism
    tvl_usd: 0
    since: 2022-09-01
    note: "wstETH bridged only"
  - chain: base
    tvl_usd: 0
    since: 2023-08-01
    note: "wstETH bridged only"
  - chain: polygon
    tvl_usd: 0
    since: 2022-09-01
    note: "wstETH bridged only"
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    assets: [stETH/ETH, wstETH/stETH]
  - id: lido_node_operators
    type: node_operator_set
    scope: [ethereum]
    note: "~30 curated operators; Consensys, P2P, Chorus One dominant"
  - id: lido_dao
    type: governance
    scope: all_deployments
    note: "LDO holders control protocol parameters, operator set, fee structure"
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    via: [wstETH restaking]
active_risks:
  - risk_id: operator_concentration
    deployment: ethereum
    note: "Top 3 operators (Consensys, P2P, Chorus One) collectively run >40% of Lido-staked ETH; correlated failure or collusion risk is material"
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "Lido withdrawal requests can take days to weeks during high demand; stETH/wstETH holders cannot redeem instantly, sustaining exchange rate dislocations"
  - risk_id: exchange_rate_vs_market_depeg
    deployment: ethereum
    note: "stETH traded at significant discount in June 2022 (Celsius unwind); wstETH bridged to L2s adds bridge latency to any re-peg arbitrage"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "LDO governance controls operator onboarding/offboarding, fee params, withdrawal credentials; hostile or compromised DAO vote could redirect validator rewards"
  - risk_id: whale_concentration
    deployment: ethereum
    note: "Lido represents ~30% of all staked ETH; a forced mass exit would exceed the exit queue capacity and depress ETH staking yield for months"
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "Operators participating in SimpleDVT or restaking via EigenLayer carry additional slashing surface beyond standard beacon-chain penalties"
audits:
  - firm: Statemind
    date: 2023-01
    url: ""
  - firm: Cantina
    date: 2023-06
    url: ""
  - firm: Quantstamp
    date: 2023-09
    url: ""
  - firm: Ackee Blockchain
    date: 2023-04
    url: ""
  - firm: MixBytes
    date: 2023-11
    url: ""
---

## Overview

Lido is the largest liquid staking protocol on Ethereum, issuing stETH (rebasing)
and wstETH (wrapped, static balance) in exchange for staked ETH. Validators are
operated by a curated set of ~30 professional node operators selected by Lido DAO.
wstETH is bridged to Arbitrum, Optimism, Base, and Polygon via canonical bridges,
making it the dominant LST collateral across DeFi.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

wstETH on L2s (Arbitrum, Optimism, Base, Polygon) is bridged, not natively issued:
- Exchange rate is sourced via Chainlink cross-chain feed; bridge latency means
  the L2 price can lag during rapid stETH market moves.
- Any L1 bridge pause (canonical bridge or protocol-level) blocks wstETH redemption
  from L2 back to L1, trapping collateral.
- No withdrawal queue on L2 — users must bridge back to Ethereum before redeeming,
  adding ≥7-day finality delay on Optimism/Base.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Node operators (active) | ~30 curated |
| Withdrawal fee | 0% (no fee) |
| Protocol fee | 10% of staking rewards → Lido DAO treasury + Node Operators |
| Min withdrawal request | 100 wei stETH |
| Max withdrawal request | 1,000 stETH per batch |
| Exit queue capacity (ETH/day) | ~57,600 ETH (8 validators/slot × 225 slots × 32 ETH, approximate) |
