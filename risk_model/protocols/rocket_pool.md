---
slug: rocket_pool
name: Rocket Pool
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 1300000000
    since: 2021-11-09
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
  - id: node_operator_network
    type: operator_set
    scope: [ethereum]
  - id: chainlink
    type: oracle_provider
    scope: [ethereum]
    assets: [rETH/ETH]
  - id: rpl_token
    type: collateral_token
    scope: [ethereum]
active_risks:
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "rETH redemption depends on beacon chain exit queue; during high exit demand, queue can stretch to weeks"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "Chainlink rETH/ETH feed — staleness during market stress can allow mispriced liquidations in dependent lending protocols"
  - risk_id: operator_concentration
    deployment: ethereum
    note: "RPL bond requirement creates economic centralization pressure; operators with large RPL stakes dominate minipool creation"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "pDAO governance controls RPL inflation rate and protocol parameters; hostile majority could redirect treasury or change fee structure"
  - risk_id: lst_lrt_depeg
    deployment: ethereum
    note: "rETH trades at discount during market stress events; secondary market price diverges from beacon chain redemption rate"
audits:
  - firm: Trail of Bits
    date: 2021-09
    url: ""
  - firm: Sigma Prime
    date: 2021-10
    url: ""
  - firm: Trail of Bits
    date: 2022-06
    url: ""
  - firm: Sigma Prime
    date: 2022-09
    url: ""
  - firm: Trail of Bits
    date: 2023-02
    url: ""
  - firm: Sigma Prime
    date: 2023-05
    url: ""
  - firm: Trail of Bits
    date: 2023-11
    url: ""
  - firm: Sigma Prime
    date: 2024-01
    url: ""
---

## Overview

Rocket Pool is a permissionless liquid staking protocol on Ethereum where node
operators post RPL token bonds (minimum 10% of ETH value) to run minipools.
Users receive rETH, an exchange-rate-accumulating LST. With ~3,000 active node
operators, Rocket Pool is significantly more decentralized than Lido but less
so than the full validator set. Total staked ETH is approximately $1.3B.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Single-chain (Ethereum only). No cross-chain deployment divergence applicable.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value | Risk note |
|-----------|-------|-----------|
| Min RPL bond | 10% of ETH value | Creates economic centralization at RPL price floor |
| rETH commission | 14% of staking rewards | Governance-adjustable |
| Withdrawal queue | Beacon chain exit queue | Up to weeks during congestion |
| Oracle type | Chainlink rETH/ETH | 24h heartbeat |
