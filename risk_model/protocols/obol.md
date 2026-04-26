---
slug: obol
name: Obol Network
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 1400000000
    since: 2023-06-01
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
  - id: lido
    type: staking_protocol
    scope: [ethereum]
    assets: [stETH]
  - id: rocket_pool
    type: staking_protocol
    scope: [ethereum]
    assets: [rETH]
  - id: validator_clusters
    type: operator_set
    scope: [ethereum]
active_risks:
  - risk_id: operator_concentration
    deployment: ethereum
    note: "DVT clusters require N/M honest operators; if threshold is breached (e.g., 3-of-5 collude), signing key is effectively compromised"
  - risk_id: governance_signer_key_leak
    deployment: ethereum
    note: "Distributed threshold signing — threshold-sized subset compromise yields full validator key"
  - risk_id: single_keeper_dependency
    deployment: ethereum
    note: "Cluster coordinator (DKG ceremony leader) is a centralization point for cluster setup and re-keying"
audits:
  - firm: Sigma Prime
    date: 2023-04
    url: ""
  - firm: Trail of Bits
    date: 2023-07
    url: ""
  - firm: Dedaub
    date: 2024-01
    url: ""
  - firm: OpenZeppelin
    date: 2024-03
    url: ""
---

## Overview

Obol Network provides Distributed Validator Technology (DVT) infrastructure for
Ethereum staking, enabling a single validator to be operated by a cluster of
nodes using threshold signatures (Charon middleware). This reduces single-point-
of-failure risk for node operators. Obol integrates with Lido, Rocket Pool, and
other staking protocols, covering ~$1.4B in staked ETH across its DVT clusters.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Single-chain (Ethereum only). No cross-chain deployment divergence applicable.
All risk is concentrated in Ethereum beacon chain liveness and validator cluster
coordination.
