---
slug: cap
name: cap (Lending)
types: [lending]
deployments:
  - chain: arbitrum
    tvl_usd: 310000000
    since: 2024-01-01
    note: "Assumed Arbitrum deployment; exact chain and launch date not publicly confirmed"
dependencies:
  - id: cap_team
    type: governance
    scope: all_deployments
    note: "cap is a new protocol; parameter control, collateral listing decisions, and upgrade authority are held by the cap team with no identified DAO or timelock"
active_risks:
  - risk_id: oracle_staleness
    deployment: all
    note: "As a new lending protocol with no public documentation, the oracle configuration — provider, heartbeat, deviation threshold, and fallback mechanism — has not been independently verified; incorrect oracle setup is the most common source of lending protocol exploit losses"
  - risk_id: deployer_key_leak
    deployment: all
    note: "No public audits have been identified for cap; contract upgrade authority and admin keys held by an unverified team represent the primary unquantified risk — a malicious or compromised upgrade could bypass collateral requirements or drain reserves"
  - risk_id: governance_hostile_decision
    deployment: all
    note: "cap has no identified governance process; all collateral listings, LTV parameters, and interest rate configurations are set unilaterally by the team. Aggressive parameter choices — or parameter changes that benefit insiders at depositor expense — cannot be contested on-chain"
  - risk_id: liquidation_bonus_too_small
    deployment: all
    note: "As a new protocol with untested collateral risk parameters, liquidation bonus calibration has not been stress-tested in live market conditions; an inadequately sized bonus reduces liquidator incentive during volatility, allowing undercollateralized positions to accumulate bad debt"
audits: []
---

## Overview

cap is a new lending protocol deployed on Arbitrum with approximately $0.31B in reported
TVL. Limited public documentation is available about its collateral types, interest rate
model, oracle configuration, or governance structure. The protocol has no identified
audit coverage. As a new lending protocol without an established audit trail or governance
framework, cap's risk profile is dominated by unverified smart contract security and
unconfirmed parameter calibration.

## Type-specific risks

See `types/lending.md` for base risk profile.
