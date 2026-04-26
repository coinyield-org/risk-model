---
slug: ssv_network
name: SSV Network
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 17200000000
    since: 2023-01-01
    note: "TVL represents ETH secured by validators running on SSV infrastructure, not protocol-owned TVL"
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
    note: "All validator duties executed on Ethereum beacon chain"
  - id: ssv_operators
    type: node_operator_set
    scope: [ethereum]
    note: "Permissionless operator marketplace; users select operator clusters for each validator"
  - id: lido
    type: staking_protocol
    scope: [ethereum]
    via: [SimpleDVT module]
    note: "Lido uses SSV for its SimpleDVT module — large portion of secured ETH"
active_risks:
  - risk_id: operator_concentration
    deployment: ethereum
    note: "A small number of SSV operators handle disproportionate validator share; correlated infrastructure failure (same cloud/DC) in a cluster could trigger slashing for all validators in that cluster"
  - risk_id: validator_key_share_compromise
    deployment: ethereum
    note: "SSV distributes validator keys via secret sharing (Shamir/BLS threshold), but threshold compromise of a cluster's operator set still enables double-signing and beacon-chain slashing"
  - risk_id: single_keeper_dependency
    deployment: ethereum
    note: "SSV relies on keeper bots for liquidating insolvent operators and distributing rewards; keeper concentration or outage delays penalty enforcement"
audits:
  - firm: SSV Network Security Team
    date: 2022-12
    url: ""
---

## Overview

SSV Network is a Distributed Validator Technology (DVT) infrastructure layer for
Ethereum staking. It splits a validator's BLS key into shares distributed across
multiple independent operators using a threshold signature scheme, reducing single-
operator failure risk. Protocols like Lido (SimpleDVT module) and solo stakers use
SSV to decentralize their validator operations. TVL figure represents the value of
ETH secured through SSV validators rather than assets held in SSV contracts.

## Type-specific risks

See `types/lst.md` for base risk profile (applied as staking infrastructure).

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Threshold scheme | 3-of-4 (minimum cluster config) |
| Operator selection | Permissionless marketplace |
| Slashing insurance | None native; relies on Ethereum slashing penalties only |
| SSV token used for | Operator fee payments, governance |
| Lido SimpleDVT share | Lido is largest single protocol consumer |
