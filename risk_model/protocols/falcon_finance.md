---
slug: falcon_finance
name: Falcon Finance
types: [synthetic]
deployments:
  - chain: ethereum
    tvl_usd: 1600000000
    since: 2024-01-01
    note: "New protocol; launch date approximate"
dependencies:
  - id: cex_venues
    type: cex_venue
    scope: all_deployments
    note: "Delta-neutral perp hedges placed on centralized exchanges; specific venues not fully disclosed"
  - id: cex_custodians
    type: custodian
    scope: all_deployments
    note: "Off-exchange custodians hold spot collateral backing CEX perp positions"
  - id: falcon_team
    type: governance
    scope: all_deployments
    note: "Falcon Finance team controls strategy, collateral allocation, and protocol parameters; no decentralized governance at launch"
active_risks:
  - risk_id: perp_funding_feedback
    deployment: ethereum
    note: "Falcon's yield depends on positive perp funding rates on CEX venues; sustained negative funding reduces collateral backing below par, creating slow-bleed undercollateralization without immediate on-chain visibility"
  - risk_id: rwa_issuer_default
    deployment: ethereum
    note: "Spot collateral is held by CEX custodians off-chain; custodian insolvency, exchange freeze, or withdrawal restriction destroys the delta-hedge backing with no on-chain recourse — analogous to the Ethena custodian model but with less track record"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "As a new protocol with limited track record, admin key infrastructure is unproven; upgrade authority and emergency controls are held by the Falcon team with no public multisig or timelock configuration disclosed"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "No decentralized governance at launch; all protocol parameter changes (collateral types, hedge venues, fee structures) are at team discretion with no on-chain checks or timelock"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "Basis price for the delta hedge depends on CEX perp funding data and spot price feeds; new protocol without established oracle redundancy increases risk of stale or manipulated pricing affecting collateral ratio calculations"
audits: []
---

## Overview

Falcon Finance is a basis-trading synthetic dollar protocol, structurally similar to Ethena USDe.
Users deposit collateral (spot ETH, BTC, or stablecoins); the protocol opens offsetting short perp
positions on centralized exchanges to create a delta-neutral book. The resulting yield (perp funding
rate minus custody costs) is passed to holders. As a recently launched protocol, governance,
custody, and oracle infrastructure are centralized and lack the track record of comparable protocols.

## Type-specific risks

See `types/synthetic.md` for base risk profile.

## Deployment divergence

Single Ethereum deployment. All material risk is on the Ethereum mainnet smart contract layer
and the off-chain CEX/custodian infrastructure. No cross-chain surface at time of assessment.
