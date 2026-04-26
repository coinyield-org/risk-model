---
slug: tbtc
name: tBTC
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 450000000
    since: 2023-01-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2023-06-01
  - chain: base
    tvl_usd: 0
    since: 2024-01-01
  - chain: polygon
    tvl_usd: 0
    since: 2023-09-01
dependencies:
  - id: threshold_network
    type: operator_set
    scope: all_deployments
    note: random beacon + threshold ECDSA wallet signing
  - id: t_stakers
    type: staking
    scope: all_deployments
    note: T token stakers selected for ECDSA wallet operators
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    assets: [BTC/USD]
active_risks:
  - risk_id: governance_signer_key_leak
    note: "Threshold ECDSA signing — compromise of enough wallet-operator keys yields ability to drain BTC backing"
  - risk_id: guardian_key_leak
    note: "Individual guardian/operator keys within the threshold set are separate attack surfaces"
  - risk_id: withdrawal_queue_delay
    note: "BTC redemption requires ECDSA wallet coordination; queue delays possible under high withdrawal demand"
  - risk_id: whale_coordination
    note: "T staker concentration affects wallet-operator selection; few large stakers dominate wallet assignment"
  - risk_id: oracle_staleness
    deployment: [arbitrum, base, polygon]
    note: "Chainlink BTC feeds on L2s subject to sequencer-dependent freshness"
audits: []
---

## Overview

tBTC v2 is a decentralized Bitcoin bridge operated by the Threshold Network.
BTC is locked in ECDSA wallets governed by a randomly selected set of T-staked
operators; the threshold signing scheme requires coordinated key material to move
funds. TVL (~$0.45B) is primarily on Ethereum. Audits were conducted by Trail of
Bits and Least Authority but PDFs are not indexed in public GitHub repositories.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Ethereum holds the primary BTC custody. Arbitrum, Base, and Polygon deployments
represent bridged tBTC — an additional bridge hop beyond the core tBTC mechanism,
compounding bridge risk. Oracle freshness on L2s depends on sequencer uptime.
