---
slug: buzz_farming
name: Buzz Farming
types: [yield_aggregator]
deployments:
  - chain: bnb
    tvl_usd: 320000000
    since: 2024-01-01
    note: "Assumed BNB Chain based on ecosystem context; no confirmed public documentation"
dependencies:
  - id: buzz_team
    type: governance
    scope: all_deployments
    note: "No public governance structure identified; protocol is operated by an anonymous or pseudonymous team"
active_risks:
  - risk_id: incentive_end_liquidity_flight
    deployment: all
    note: "Buzz Farming's TVL is characteristic of incentive-driven farming — high APY farming vaults attract mercenary capital that exits rapidly when reward emissions end or are diluted; without a durable yield source, TVL is structurally transient"
  - risk_id: deployer_key_leak
    deployment: all
    note: "No audits and no public smart contract documentation have been identified; admin and upgrade keys are held by an unknown team, creating full exposure to rug pull or malicious upgrade — funds could be redirected without warning"
  - risk_id: governance_hostile_decision
    deployment: all
    note: "Absence of on-chain governance means all parameter decisions — emission rates, vault allocations, fee structures — are made unilaterally by the team; there is no mechanism for depositors to contest or reverse adverse decisions"
audits: []
---

## Overview

Buzz Farming is a yield farming protocol operating primarily in the BNB Chain ecosystem
with approximately $0.32B in reported TVL. No public documentation, audit reports,
whitepaper, or governance structure have been identified. The protocol appears to be
a farming aggregator or incentivized vault product, but the underlying yield source,
smart contract architecture, and team identity are not publicly disclosed. Risk profile
is dominated by complete opacity, absence of audits, and structurally incentive-driven TVL.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.
