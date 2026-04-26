---
slug: fluid_lending
name: Fluid Lending (Instadapp)
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 710000000
    since: 2024-01-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-01-01
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: instadapp
    type: governance
    scope: all_deployments
  - id: underlying_collateral_tokens
    type: collateral
    scope: all_deployments
active_risks:
  - risk_id: oracle_staleness
    deployment: [ethereum, arbitrum]
    note: "Chainlink feed staleness affects liquidation triggers; on Arbitrum, sequencer downtime compounds oracle lag"
  - risk_id: deployer_key_leak
    deployment: all_deployments
    note: "Instadapp controls upgrades on a private repo — changes cannot be reviewed on-chain before execution; key compromise enables silent protocol modification"
  - risk_id: governance_hostile_decision
    deployment: all_deployments
    note: "Instadapp team retains unilateral upgrade and parameter authority; private repo makes pre-execution review impossible for external stakeholders"
  - risk_id: whale_concentration
    deployment: all_deployments
    note: "Concentrated large depositors can trigger utilization spikes or coordinated withdrawals affecting protocol liquidity"
audits: []
---

## Overview

Fluid Lending is an overcollateralized lending protocol developed by the Instadapp team. It operates on Ethereum and Arbitrum with Chainlink price feeds for liquidation triggers. The protocol's smart contracts are maintained in a private repository, which limits external review of changes prior to deployment.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Arbitrum deployment has additional surface:
- Sequencer downtime can delay oracle updates and prevent timely liquidation — the protocol's handling of sequencer uptime feeds should be verified
- Arbitrum gas fee spikes during congestion may render small liquidations uneconomical

The private repository is a structural opacity risk across all deployments: upgrades cannot be independently reviewed before they go live, which increases reliance on Instadapp's internal security process.

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Oracle | Chainlink (all assets) |
| Upgrade authority | Instadapp team (private repo) |
| Code transparency | Private repository — no public pre-review |
