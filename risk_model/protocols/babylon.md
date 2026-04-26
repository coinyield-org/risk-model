---
slug: babylon
name: Babylon Protocol
types: [lrt]
deployments:
  - chain: bitcoin
    tvl_usd: 4000000000
    since: 2024-08-01
    note: "BTC staking layer; staking scripts lock BTC natively on Bitcoin"
  - chain: ethereum
    tvl_usd: 0
    since: 2024-08-01
    note: "Governance and finality gadget coordination; no direct user TVL"
dependencies:
  - id: bitcoin_miners
    type: validator_set
    scope: [bitcoin]
    note: "Bitcoin PoW provides finality for staked BTC; Babylon inherits Bitcoin's security model"
  - id: babylon_team
    type: governance
    scope: all_deployments
    note: "Babylon team controls protocol parameter upgrades and PoS chain integrations in current phase"
  - id: pos_consumer_chains
    type: restaking_protocol
    scope: all_deployments
    note: "PoS chains that consume BTC security via Babylon; their slashing conditions define the risk surface"
active_risks:
  - risk_id: validator_avs_slashing
    deployment: bitcoin
    note: "BTC slashing conditions (double-sign on Babylon-secured PoS chains) are novel and untested in production at scale; a slashing event permanently destroys the underlying BTC with no recovery mechanism"
  - risk_id: governance_hostile_decision
    deployment: bitcoin
    note: "Babylon team controls critical protocol parameters in the current phase including staking script versions, finality provider onboarding, and consumer chain allowlist; a hostile or compromised team could alter slashing rules"
  - risk_id: deployer_key_leak
    deployment: bitcoin
    note: "BTC staking scripts require key management for the staker extraction path; compromise of finality provider keys or the Babylon covenant committee keys enables unauthorized BTC extraction or forced slashing"
  - risk_id: fallback_oracle_misconfig
    deployment: bitcoin
    note: "Pricing BTC staking positions (e.g. liquid staking tokens issued on top of Babylon) relies on novel oracle configurations with limited market history; no established oracle infrastructure covers BTC-native staking yields"
audits: []
---

## Overview

Babylon enables native BTC staking without bridging: BTC holders lock funds in
Bitcoin-native scripts (using covenant emulation via adaptor signatures) to provide
cryptoeconomic security to external PoS chains. Staked BTC earns yield from secured chains.
Slashing is enforced through pre-signed Bitcoin transactions that burn or redirect BTC if
a finality provider double-signs. The protocol is in early phases with Babylon team controlling
key governance levers; decentralization is staged over multiple phases.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Bitcoin chain carries all staked value; slashing and extraction logic lives entirely in
Bitcoin script with no EVM smart-contract layer. Ethereum is used only for governance
coordination in the current phase. This creates an asymmetric risk profile: the security
model depends on Bitcoin scripting correctness (covenant committee) rather than audited
EVM contracts, and the tooling for formal verification of Bitcoin scripts is immature.
