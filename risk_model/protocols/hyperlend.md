---
slug: hyperlend
name: HyperLend Pooled
types: [lending]
deployments:
  - chain: hyperliquid_l1
    tvl_usd: 350000000
    since: 2024-06-01
    note: "Deployed on HyperEVM, the EVM-compatible execution layer of Hyperliquid L1"
dependencies:
  - id: hyperliquid_chain
    type: underlying_chain
    scope: [hyperliquid_l1]
    note: "HyperLend runs on HyperEVM; chain liveness, finality, and sequencer behavior are entirely controlled by Hyperliquid validators"
  - id: hype_oracle
    type: oracle_provider
    scope: [hyperliquid_l1]
    note: "Price feeds on HyperEVM are sourced from the Hyperliquid validator set — the same entities producing blocks; there is no independent oracle provider"
  - id: hyperlend_team
    type: governance
    scope: [hyperliquid_l1]
    note: "HyperLend is a newly deployed protocol; parameter control and upgrade authority are held by the HyperLend team with no identified DAO or timelock"
active_risks:
  - risk_id: oracle_staleness
    deployment: hyperliquid_l1
    note: "HyperLend relies on price feeds provided by Hyperliquid validators rather than an independent oracle network; validator collusion, network congestion, or consensus issues could result in stale or manipulated prices used for liquidation thresholds, creating bad debt risk"
  - risk_id: chain_halt
    deployment: hyperliquid_l1
    note: "Hyperliquid L1 is a proprietary PoS chain with a limited validator set; a consensus failure or coordinated validator outage halts block production, preventing liquidations and withdrawals — positions cannot be managed during a halt regardless of collateral health"
  - risk_id: deployer_key_leak
    deployment: hyperliquid_l1
    note: "HyperLend has no public audits; contract upgrade authority and admin controls have not been independently verified. A compromised admin key could modify collateral parameters, disable liquidations, or redirect protocol fees"
  - risk_id: governance_hostile_decision
    deployment: hyperliquid_l1
    note: "HyperLend parameter decisions (LTV ratios, collateral listings, interest rate curves) are made by the HyperLend team without a public governance process; hostile or mistaken parameter changes could create systemic undercollateralization"
  - risk_id: whale_concentration
    deployment: hyperliquid_l1
    note: "As a new lending protocol on a single proprietary chain, HyperLend TVL is likely concentrated among a small number of large depositors; coordinated withdrawal by whale LPs would trigger utilization spikes, blocking borrower withdrawals and creating bank-run dynamics"
audits: []
---

## Overview

HyperLend is a pooled lending protocol deployed on HyperEVM, the EVM-compatible execution
layer of Hyperliquid L1. It enables borrowing and lending of assets within the Hyperliquid
ecosystem. As a new protocol on a proprietary chain, HyperLend inherits all of Hyperliquid's
chain-level risks — including validator-controlled oracle feeds, a non-standard consensus
mechanism, and limited chain maturity — while adding its own lending-specific risks around
collateral management and liquidation mechanics.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Key parameters (hyperliquid_l1, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Oracle source | Hyperliquid validator set (not independent) |
| Chain | HyperEVM (Hyperliquid L1) |
| Audit coverage | None identified |
| Governance | HyperLend team (no DAO) |
