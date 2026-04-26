---
slug: optimism_bridge
name: Optimism Bridge (Canonical)
primary: coinbase_bridge
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 520000000
    since: 2021-12-16
    note: "L1 lock side; canonical OP Stack bridge for Optimism mainnet"
  - chain: optimism
    tvl_usd: 0
    since: 2021-12-16
    note: "L2 side; value reflected in Ethereum-side lock"
dependencies:
  - id: op_foundation_sequencer
    type: sequencer
    scope: [optimism]
    note: "OP Foundation operates the sole Optimism mainnet sequencer"
  - id: optimism_op_stack
    type: codebase
    scope: [ethereum, optimism]
    note: "Shares OP Stack codebase with Base, Mode, Zora, and other Superchain members"
  - id: op_foundation_multisig
    type: governance
    scope: [ethereum, optimism]
    note: "OP Foundation multisig holds upgrade authority over L1 bridge proxy contracts"
active_risks:
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "Same OP Stack proxy upgrade risk as coinbase_bridge; OP Foundation multisig controls L1 StandardBridge and OptimismPortal upgrade authority"
  - risk_id: bridge_pause_censorship
    deployment: [ethereum, optimism]
    note: "OptimismPortal guardian (OP Foundation-controlled) can pause deposits and withdrawals; same risk vector as coinbase_bridge"
  - risk_id: per_deployment_divergence
    deployment: optimism
    note: "Superchain shared codebase means a critical bug discovered in OP Stack propagates simultaneously to all Superchain members (Base, Optimism, Mode, Zora, etc.) — systemic exposure is broader than any single bridge"
audits: []
---

## Overview

The Optimism Bridge is the canonical L1↔L2 bridge for Optimism mainnet, built on
the OP Stack and sharing its core smart contract architecture with Base and other
Superchain members. It uses the same OptimismPortal, L1StandardBridge, and fault
dispute game contracts as coinbase_bridge. The OP Foundation operates the sequencer
and holds upgrade authority.

## Type-specific risks

See `types/bridge.md` for base risk profile. See also `coinbase_bridge.md` for
full OP Stack risk analysis — this protocol shares the same codebase and trust model.

## Deployment divergence

Shares OP Stack risks with `coinbase_bridge` (see that file for full analysis). The
key additional risk specific to Optimism Bridge is Superchain codebase concentration:
a single critical bug in OP Stack would affect Optimism, Base, Mode, Zora, and all
other Superchain members simultaneously. The blast radius of any OP Stack exploit is
proportional to the combined TVL of all Superchain deployments, not just Optimism.
