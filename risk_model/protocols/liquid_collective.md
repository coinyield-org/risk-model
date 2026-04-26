---
slug: liquid_collective
name: Liquid Collective
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 820000000
    since: 2023-01-01
dependencies:
  - id: ethereum_beacon_chain
    type: infrastructure
    scope: all_deployments
  - id: alluvial
    type: governance
    scope: all_deployments
  - id: coinbase
    type: node_operator
    scope: all_deployments
  - id: figment
    type: node_operator
    scope: all_deployments
  - id: staked
    type: node_operator
    scope: all_deployments
active_risks:
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "Ethereum beacon chain withdrawal queue can extend during validator exit congestion; LsETH redemption pace is queue-dependent"
  - risk_id: quoted_vs_underlying_depeg
    deployment: ethereum
    note: "LsETH market price may deviate from exchange rate if secondary liquidity is thin — institutional-only operator set limits arb capacity"
  - risk_id: governance_signer_key_leak
    deployment: ethereum
    note: "Alluvial multisig controls protocol upgrades and operator set changes; compromise enables unauthorized parameter changes"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "Alluvial/AlluvialFinance governance can add or remove node operators and change protocol parameters unilaterally"
audits:
  - firm: Halborn
    date: 2023-01
    url: ""
---

## Overview

Liquid Collective is an institutional liquid staking protocol on Ethereum, governed by AlluvialFinance. ETH deposits are delegated exclusively to a curated set of institutional node operators (Coinbase, Figment, Staked, and others). The LsETH token represents a claim on staked ETH plus accumulated rewards and is designed for regulated institutional use.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

No multi-chain deployment. All staking activity occurs on Ethereum mainnet; LsETH is a single-chain token.

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Operator set | Institutional only (Coinbase, Figment, Staked, etc.) |
| Operator selection | Alluvial governance |
| Withdrawal mechanism | Ethereum beacon chain exit queue |
| Upgrade authority | Alluvial multisig |
