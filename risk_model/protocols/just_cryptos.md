---
slug: just_cryptos
name: JustCryptos / JUST (TRON)
types: [bridge]
deployments:
  - chain: tron
    tvl_usd: 2500000000
    since: 2020-09-01
    note: "TRON-based wrapped asset bridge; majority of TVL is USDT bridged to TRON"
dependencies:
  - id: tron_foundation
    type: governance
    scope: all_deployments
    note: "TRON Foundation and Justin Sun exercise effective governance control over the JUST ecosystem"
  - id: justin_sun
    type: key_individual
    scope: all_deployments
    note: "Justin Sun is the dominant governance actor; his statements and actions directly impact protocol parameters and asset reserves"
  - id: tron_super_representatives
    type: validator_set
    scope: all_deployments
    note: "27 Super Representatives (elected) validate TRON chain; validator set is closely aligned with TRON Foundation"
  - id: tether
    type: issuer
    scope: all_deployments
    assets: [USDT]
    note: "USDT on TRON is a Tether-issued asset; the majority of JUST bridge TVL is USDT"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: tron
    note: "TRON Foundation and Justin Sun hold effective veto and initiative power over the JUST protocol. Unilateral parameter changes, asset freezes, or migration decisions can be executed without broad community consensus."
  - risk_id: deployer_key_leak
    deployment: tron
    note: "The JUST protocol lacks transparent multisig governance. Admin keys with upgrade and pause authority are not publicly documented. Compromise of admin keys could enable draining of the $2.5B TVL."
  - risk_id: whale_concentration
    deployment: tron
    note: "Justin Sun and the TRON Foundation collectively control a dominant share of TRON governance power via Super Representative influence. This concentration creates a single point of governance failure."
  - risk_id: oracle_coverage_absence
    deployment: tron
    note: "TRON chain lacks a mature, decentralized oracle infrastructure comparable to Chainlink on Ethereum. Asset prices and peg mechanisms on TRON rely on less audited or centralized price feeds."
audits: []
---

## Overview

JustCryptos (JUST) is a TRON-based bridge and DeFi ecosystem providing wrapped asset
issuance and liquidity. The majority of its $2.5B TVL consists of USDT bridged to the
TRON network. Governance is effectively controlled by the TRON Foundation and Justin
Sun, with 27 Super Representatives acting as validators. The protocol has no publicly
available audit PDFs; governance transparency is materially lower than comparable
Ethereum-based bridges.

## Type-specific risks

See `types/bridge.md` for base risk profile.
