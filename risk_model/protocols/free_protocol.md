---
slug: free_protocol
name: Free Protocol
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 310000000
    since: 2024-01-01
    note: "Chain attribution is uncertain; no confirmed public documentation of deployment chain(s)"
dependencies:
  - id: free_protocol_team
    type: governance
    scope: all_deployments
    note: "No public governance structure, DAO, or documentation identified; protocol is operated by an unidentified team"
active_risks:
  - risk_id: bridge_lock_backing_loss
    deployment: all
    note: "Free Protocol operates as a bridge with locked assets; the absence of any public documentation or audits means the lock-and-mint mechanism, reserve custody, and bridge signing authority are entirely unverified — backing loss via exploit or misappropriation cannot be ruled out"
  - risk_id: deployer_key_leak
    deployment: all
    note: "No audits and no public smart contract documentation have been identified for Free Protocol; upgrade authority and bridge operator keys are held by unknown parties, creating an unquantified but material key compromise and rug pull risk"
  - risk_id: oracle_staleness
    deployment: all
    note: "No public information exists about Free Protocol's asset pricing or valuation methodology; without a documented oracle, backing verification and detection of reserve shortfalls is impossible for external observers"
audits: []
---

## Overview

Free Protocol is a bridge protocol with approximately $0.31B in reported TVL. No public
documentation, whitepaper, audit reports, or governance structure have been identified.
The protocol's chain deployments, bridging mechanism, asset custody model, and team
identity are not publicly disclosed. Risk profile is dominated by complete opacity of
operations and custody, analogous to UniRouter (#90). Independent risk assessment is not
possible without public technical documentation.

## Type-specific risks

See `types/bridge.md` for base risk profile.
