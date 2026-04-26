---
slug: coinbase_bridge
name: Coinbase Bridge (OP Stack / Base)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 5600000000
    since: 2023-08-09
    note: "TVL represents assets locked in the L1 bridge contract awaiting finalization or held as canonical Base collateral"
  - chain: base
    tvl_usd: 0
    since: 2023-08-09
    note: "L2 side; value is reflected in Ethereum-side lock"
dependencies:
  - id: optimism_op_stack
    type: codebase
    scope: [ethereum, base]
    note: "Base is an OP Stack L2; inherits Optimism canonical bridge contracts and fault proof system"
  - id: coinbase_sequencer
    type: sequencer
    scope: [base]
    note: "Coinbase operates the sole Base sequencer; centralized ordering and inclusion authority"
  - id: base_fault_proof
    type: dispute_resolution
    scope: [ethereum, base]
    note: "Cannon-based fault proof system deployed on Base in 2024; allows permissionless challenge of invalid state roots"
  - id: coinbase_multisig
    type: governance
    scope: [ethereum, base]
    note: "Coinbase-controlled multisig holds proxy upgrade authority for L1 bridge contracts"
active_risks:
  - risk_id: sequencer_centralization
    deployment: base
    note: "Coinbase is the sole sequencer for Base; it can reorder transactions (MEV extraction), delay inclusion, or go offline — users must wait for L1 force-inclusion mechanism (7-day window) if sequencer censors them"
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "The L1 StandardBridge and OptimismPortal are upgradeable proxies controlled by a Coinbase multisig; an unauthorized or coerced upgrade could redirect locked funds or modify withdrawal verification logic"
  - risk_id: per_deployment_profile_divergence
    deployment: base
    note: "Base operates with Coinbase-specific configuration diverging from Optimism mainnet: different guardian thresholds, separate Security Council composition, and Coinbase-negotiated fee parameters — risk analysts must treat it as a distinct deployment, not a vanilla OP Stack instance"
  - risk_id: bridge_pause_censorship
    deployment: [ethereum, base]
    note: "The OptimismPortal has a guardian role (Coinbase-controlled) that can pause deposits and withdrawals; a paused bridge traps funds on L2 until governance unpauses — users have no recourse during the pause window"
audits:
  - firm: Trail of Bits
    date: 2023-05
    url: ""
  - firm: Spearbit
    date: 2023-06
    url: ""
  - firm: OpenZeppelin
    date: 2023-07
    url: ""
  - firm: Sigma Prime
    date: 2024-01
    url: ""
---

## Overview

The Coinbase Bridge is the canonical L1↔L2 bridge for Base, an OP Stack L2
operated by Coinbase. It uses the same smart contract architecture as the
Optimism canonical bridge (OptimismPortal, L1StandardBridge, L2OutputOracle / fault
dispute game), with Coinbase acting as sequencer and upgrade authority. The Cannon
fault proof system went live on Base in 2024, enabling permissionless state root
challenges, but the sequencer and bridge contracts remain under Coinbase multisig
control.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Base shares OP Stack code with Optimism mainnet but differs in:
- Sequencer operator: Coinbase (Base) vs OP Labs / Optimism Foundation (Optimism)
- Security Council composition and threshold: Base has its own guardian configuration
- Upgrade timelock: Coinbase multisig timelock may differ from Optimism Superchain defaults
- Fee parameters: negotiated separately between Coinbase and OP Foundation

Analysts should not assume identical risk profile to Optimism or other OP Stack chains.

## Key parameters (ethereum → base, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Sequencer | Coinbase (sole) |
| Withdrawal finalization delay | 7 days (fault proof challenge window) |
| Bridge upgrade authority | Coinbase multisig |
| Fault proof system | Cannon (live since 2024) |
| Force-inclusion window | 12 hours (L1 deposit via OptimismPortal) |
| Guardian (pause authority) | Coinbase-controlled |
