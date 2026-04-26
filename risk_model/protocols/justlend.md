---
slug: justlend
name: JustLend
types: [lending]
deployments:
  - chain: tron
    tvl_usd: 3600000000
    since: 2020-11-01
dependencies:
  - id: tron_validators
    type: validator_set
    scope: [tron]
    note: "27 Super Representatives elected by TRX stakers; Binance and Justin Sun-aligned entities hold material voting power"
  - id: tron_foundation
    type: governance
    scope: [tron]
    note: "TRON Foundation controls key protocol infrastructure and can influence validator election"
  - id: tronDAO
    type: governance
    scope: [tron]
    note: "TronDAO governance, heavily influenced by Justin Sun's TRX holdings"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: tron
    note: "TronDAO governance and Justin Sun's concentrated TRX holdings give a small group near-unilateral control over JustLend risk parameters, interest rate models, and asset listings; a hostile or coerced governance action could redirect reserves or modify collateral factors adversely"
  - risk_id: oracle_staleness
    deployment: tron
    note: "TRON oracle infrastructure is substantially less mature and decentralized than Ethereum equivalents; fewer node operators and lower redundancy increase the risk of stale or manipulated price feeds during volatile markets"
  - risk_id: whale_coordination
    deployment: tron
    note: "Justin Sun is documented as a large depositor across JustLend markets; coordinated large withdrawals or borrow actions by a small set of insiders could trigger utilization spikes or deplete specific reserves"
  - risk_id: deployer_key_leak
    deployment: tron
    note: "Admin key control over JustLend contracts is concentrated; on TRON, multisig tooling and key management standards lag Ethereum, increasing the risk of a compromised upgrade key"
  - risk_id: delegate_single_point_failure
    deployment: tron
    note: "TRON's 27 Super Representatives constitute a narrow validator set; several SRs are controlled by entities closely tied to Justin Sun, creating correlated failure risk for chain liveness and censorship resistance"
audits: []
---

## Overview

JustLend is the dominant lending protocol on TRON, operating with similar mechanics to
Aave V2 (supply/borrow against overcollateralized positions, interest rate kinks, liquidation
bonuses). TVL is concentrated in USDT and TRX. The protocol operates under TRON's governance
model where 27 elected Super Representatives validate the chain — a materially more centralized
trust model than Ethereum. Justin Sun's influence over TronDAO and TRON Foundation creates
concentrated governance risk at the protocol and chain level simultaneously.

## Type-specific risks

See `types/lending.md` for base risk profile.
