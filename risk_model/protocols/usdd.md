---
slug: usdd
name: USDD (TRON)
types: [cdp]
deployments:
  - chain: tron
    tvl_usd: 1300000000
    since: 2022-05-05
dependencies:
  - id: tron_foundation
    type: governance_actor
    scope: [tron]
  - id: trx_token
    type: collateral_token
    scope: [tron]
  - id: tron_super_representatives
    type: operator_set
    scope: [tron]
active_risks:
  - risk_id: whale_concentration
    deployment: tron
    note: "Justin Sun controls a large portion of TRX supply; coordinated sell pressure would erode USDD collateral ratio"
  - risk_id: governance_hostile_decision
    deployment: tron
    note: "TronDAO governance is effectively controlled by TRON Foundation; parameter changes (collateral ratio, peg defense) lack credible checks"
  - risk_id: overcollateral_ratio_erosion
    deployment: tron
    note: "TRX price decline directly reduces collateralization; peg defense mechanism relies on TRX buy-backs funded by TRON Foundation reserves"
  - risk_id: oracle_coverage_absence
    deployment: tron
    note: "TRON chain oracle infrastructure is significantly less mature than Ethereum; no Chainlink deployment on TRON mainnet"
  - risk_id: thin_liquidity_source_manipulation
    deployment: tron
    note: "USDD liquidity is thin on TRON DEXes; secondary market peg maintenance depends heavily on TRON Foundation intervention"
audits: []
---

## Overview

USDD is a TRC-20 algorithmic/CDP stablecoin issued on the TRON blockchain,
backed by TRX and managed by the TRON DAO Reserve. It was launched in May 2022
during a period heavily influenced by UST/LUNA's collapse. The peg mechanism
combines TRX over-collateralization with discretionary reserve interventions by
the TRON Foundation and Justin Sun. Circulating supply is approximately $1.3B.

## Type-specific risks

See `types/cdp.md` for base risk profile.

## Deployment divergence

Single-chain (TRON only). TRON's 27 Super Representatives (SR) consensus model
concentrates block production and censorship power to a small set of entities,
many of which have ties to the TRON Foundation. This represents a materially
different trust model than Ethereum-based CDPs. There is no credible external
oracle provider and no published audit of USDD smart contracts.

## Key parameters (tron, as of 2026-01)

| Parameter | Value | Risk note |
|-----------|-------|-----------|
| Collateral | TRX + TRON Foundation reserves | Subject to Justin Sun's discretion |
| Collateral ratio | ~200%+ (stated) | Not independently verifiable |
| Oracle | Internal / TRON Foundation | No external oracle provider |
| Governance | TronDAO (27 SRs) | Effectively TRON Foundation controlled |
