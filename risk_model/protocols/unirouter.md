---
slug: unirouter
name: UniRouter
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 320000000
    since: 2024-01-01
    note: "Chain attribution is uncertain; no confirmed public documentation of deployment chain(s)"
dependencies:
  - id: unirouter_team
    type: governance
    scope: all_deployments
    note: "No public governance structure, DAO, or documentation identified; the protocol team controls all protocol operations"
active_risks:
  - risk_id: bridge_lock_backing_loss
    deployment: all
    note: "UniRouter operates as a bridge with locked assets on source chains; the absence of any public documentation or audits means the lock-and-mint mechanism, reserve custody, and bridge signing authority are entirely unverified — backing loss via exploit or misappropriation cannot be ruled out"
  - risk_id: deployer_key_leak
    deployment: all
    note: "No audits and no public smart contract documentation have been identified for UniRouter; upgrade authority and bridge operator keys are held by unknown parties, creating an unquantified but material key compromise risk"
  - risk_id: oracle_staleness
    deployment: all
    note: "No public information exists about UniRouter's price feed or asset valuation methodology; without a documented oracle, accurate pricing of bridged assets and detection of backing divergence is impossible for external observers"
audits: []
---

## Overview

UniRouter is a bridge protocol with approximately $0.32B in reported TVL. No public
documentation, whitepaper, audit reports, or governance structure have been identified.
The protocol's chain deployments, bridging mechanism, asset custody model, and team
identity are not publicly disclosed. The absence of public information makes independent
risk assessment impossible; the risk profile is dominated by complete opacity of
operations and custody.

## Type-specific risks

See `types/bridge.md` for base risk profile.
