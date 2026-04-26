---
slug: meth_protocol
name: mETH Protocol (Mantle)
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 680000000
    since: 2023-12-01
  - chain: mantle
    tvl_usd: 0
    since: 2024-01-01
dependencies:
  - id: ethereum_beacon_chain
    type: infrastructure
    scope: [ethereum]
  - id: mantle_team
    type: node_operator
    scope: all_deployments
  - id: mantle_l2
    type: bridge
    scope: [mantle]
    assets: [mETH]
  - id: mnt_governance
    type: governance
    scope: all_deployments
active_risks:
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "Ethereum beacon chain withdrawal queue applies; redemption pace is capped by validator exit limits"
  - risk_id: quoted_vs_underlying_depeg
    deployment: [ethereum, mantle]
    note: "mETH market price may diverge from exchange rate on both Ethereum and Mantle; Mantle's thin liquidity amplifies divergence"
  - risk_id: governance_hostile_decision
    deployment: all_deployments
    note: "Mantle DAO controls protocol governance; DAO decisions can alter operator set, fee structure, and upgrade schedule"
  - risk_id: l2_sequencer_dep
    deployment: mantle
    note: "Mantle is an OP Stack L2 with a centralized sequencer; sequencer downtime or censorship affects mETH usability on Mantle"
audits:
  - firm: Zellic
    date: 2023-12
    url: ""
---

## Overview

mETH Protocol is a liquid staking protocol developed by the Mantle team. ETH is staked on the Ethereum beacon chain via validators operated by the Mantle team; mETH tokens represent staked ETH plus rewards. mETH is distributed and used on both Ethereum and the Mantle L2, an OP Stack chain with a centralized sequencer.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Two-chain deployment creates distinct risk layers:
- Ethereum: staking occurs here — beacon chain withdrawal queue, validator slashing, and operator concentration (Mantle team) are the primary risks
- Mantle L2: mETH is bridged via the Mantle native bridge; the OP Stack sequencer is centralized — downtime or censorship disrupts mETH transfers and DeFi composability on Mantle; finality delay means bridge withdrawals to Ethereum take ~7 days

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Validator operator | Mantle team (centralized) |
| Withdrawal mechanism | Ethereum beacon chain exit queue |
| Mantle bridge | Mantle native bridge (OP Stack) |
| Mantle sequencer | Centralized (Mantle team) |
| Governance | Mantle DAO (MNT token) |
