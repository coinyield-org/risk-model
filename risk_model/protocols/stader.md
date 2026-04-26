---
slug: stader
name: Stader Labs
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 700000000
    since: 2023-01-12
  - chain: polygon
    tvl_usd: 300000000
    since: 2022-06-01
  - chain: bnb
    tvl_usd: 200000000
    since: 2022-08-01
  - chain: avalanche
    tvl_usd: 100000000
    since: 2022-09-01
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
  - id: chainlink
    type: oracle_provider
    scope: [ethereum, polygon, bnb, avalanche]
  - id: node_operator_network
    type: operator_set
    scope: [ethereum, polygon, bnb, avalanche]
active_risks:
  - risk_id: operator_concentration
    deployment: [ethereum, polygon, bnb, avalanche]
    note: "Each chain's node operator set is independent and smaller than Lido/Rocket Pool; permissioned operator lists on some chains"
  - risk_id: lst_lrt_depeg
    deployment: [ethereum, polygon, bnb, avalanche]
    note: "ETHx, MaticX, BNBx each have independent market liquidity; thinner pools mean larger depeg during stress"
  - risk_id: withdrawal_queue_delay
    deployment: [ethereum, polygon, bnb, avalanche]
    note: "Each chain has different validator exit queue mechanics; BNB chain 7-day unbonding period is distinct from Ethereum"
  - risk_id: per_deployment_divergence
    deployment: [polygon, bnb, avalanche]
    note: "Each deployment (ETHx, MaticX, BNBx, AVAX) has a different operator set, oracle, liquidity depth, and withdrawal mechanism"
audits:
  - firm: Sigma Prime
    date: 2022-12
    url: ""
  - firm: Halborn
    date: 2023-01
    url: ""
  - firm: Code4rena
    date: 2023-02
    url: ""
  - firm: Sigma Prime
    date: 2023-04
    url: ""
  - firm: Halborn
    date: 2023-06
    url: ""
  - firm: Code4rena
    date: 2023-08
    url: ""
  - firm: Sigma Prime
    date: 2023-10
    url: ""
  - firm: Halborn
    date: 2023-11
    url: ""
  - firm: Code4rena
    date: 2024-01
    url: ""
  - firm: Sigma Prime
    date: 2024-02
    url: ""
  - firm: Halborn
    date: 2024-03
    url: ""
  - firm: Code4rena
    date: 2024-05
    url: ""
  - firm: Sigma Prime
    date: 2024-07
    url: ""
---

## Overview

Stader Labs is a multi-chain liquid staking protocol offering LST products
across Ethereum (ETHx), Polygon (MaticX), BNB Chain (BNBx), and Avalanche.
Each deployment operates independently with its own operator set, token, and
withdrawal mechanism. Total TVL across all deployments is approximately $1.3B,
with Ethereum ETHx being the largest by value.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Each chain deployment has a materially different risk profile:
- Ethereum (ETHx): permissioned operator set, Chainlink oracle, beacon chain exit queue
- Polygon (MaticX): MATIC staking via Polygon PoS checkpoint system; different exit mechanics
- BNB Chain (BNBx): 21-validator BNB chain with 7-day unbonding; BSC oracle fewer node operators
- Avalanche: smaller operator set, thinner AVAX LST liquidity, Avalanche validator rotation

## Key parameters (per deployment, as of 2026-01)

| Deployment | LST | Operator model | Withdrawal | Oracle |
|-----------|-----|---------------|------------|--------|
| Ethereum | ETHx | Permissioned | Beacon exit queue | Chainlink ETH/USD |
| Polygon | MaticX | Permissioned | Polygon checkpoint | Chainlink MATIC/USD |
| BNB | BNBx | Permissioned | 7-day unbonding | Chainlink BNB/USD |
| Avalanche | AVAX LST | Permissioned | Avalanche unlock | Chainlink AVAX/USD |
