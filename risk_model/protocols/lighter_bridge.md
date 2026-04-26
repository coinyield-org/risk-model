---
slug: lighter_bridge
name: Lighter Bridge
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 500000000
    since: 2024-01-01
    note: "Estimated chain based on TVL distribution; no public deployment documentation confirmed"
dependencies:
  - id: lighter_team
    type: governance
    scope: all_deployments
    note: "New protocol; no public governance documentation. Assumed team-controlled admin keys"
active_risks:
  - risk_id: bridge_lock_backing_loss
    deployment: ethereum
    note: "Assets locked in bridge escrow are at risk from contract vulnerabilities or admin key abuse. No public audit has been indexed; the integrity of the escrow mechanism cannot be independently verified"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "No public documentation of multisig structure or upgrade authority. A team-controlled EOA or low-threshold multisig over bridge admin functions represents existential risk to all locked funds"
  - risk_id: guardian_key_leak
    deployment: ethereum
    note: "Pause or guardian key surface is undocumented; a compromised guardian key could freeze withdrawals or redirect funds without on-chain recourse for users"
  - risk_id: oracle_coverage_absence
    deployment: ethereum
    note: "No public information on oracle or asset validation mechanisms. New protocol with no verified audit trail; cross-chain accounting integrity is unverifiable from public information"
audits: []
---

## Overview

Lighter Bridge is a cross-chain bridge protocol with approximately $500M TVL as of
early 2026. No public GitHub repository, audit reports, or detailed technical
documentation have been identified. The risk profile is derived from structural
bridge archetypes. Analysts should treat this protocol with elevated caution until
audit reports and contract documentation are publicly available.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Deployment chain estimated as Ethereum based on TVL; cross-chain counterparty chains
are unconfirmed. Deployment divergence analysis is not possible without public
technical documentation.
