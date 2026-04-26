---
slug: solstice_usx
name: Solstice USX
types: [synthetic]
deployments:
  - chain: ethereum
    tvl_usd: 380000000
    since: 2024-01-01
dependencies:
  - id: cex_venues
    type: operator
    scope: all_deployments
    note: centralized exchanges used for delta-hedge perp positions
  - id: custodians
    type: custodian
    scope: all_deployments
    note: off-chain custodians hold collateral backing CEX positions
  - id: solstice_team
    type: governance
    scope: all_deployments
active_risks:
  - risk_id: perp_funding_feedback
    note: "Basis trading strategy depends on positive perp funding; sustained negative funding erodes USX backing and can break the peg"
  - risk_id: guardian_key_leak
    note: "Off-chain custodians hold collateral for CEX positions; custodian key compromise or default = loss of delta-hedge backing"
  - risk_id: deployer_key_leak
    note: "New protocol with no public audits; upgrade authority is centralized and key compromise allows arbitrary changes to minting logic"
  - risk_id: oracle_staleness
    note: "USX peg relies on accurate price feeds for collateral valuation; stale or manipulated oracles misprices backing"
  - risk_id: self_fulfilling_depeg
    note: "USX depeg fear triggers withdrawals; if redemption requires unwinding CEX positions under stress, execution risk amplifies the depeg"
audits: []
---

## Overview

Solstice USX is a synthetic dollar protocol (~$0.38B TVL) using a basis trading
strategy: user deposits are collateralizing perp short positions on centralized
exchanges to create a delta-neutral USD exposure. The USX peg depends on sustained
positive funding rates, reliable custodians, and CEX solvency — risks that are
structurally similar to Ethena's USDe but with no public audits and a shorter track
record. The absence of audits and the centralized key structure make this a
high-operational-risk protocol.

## Type-specific risks

See `types/synthetic.md` for base risk profile.
