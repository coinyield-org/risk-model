---
slug: lombard_lbtc
name: Lombard LBTC
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 780000000
    since: 2024-01-01
  - chain: bnb
    tvl_usd: 0
    since: 2024-01-01
  - chain: base
    tvl_usd: 0
    since: 2024-01-01
dependencies:
  - id: babylon_protocol
    type: restaking_protocol
    scope: all_deployments
  - id: lombard_multisig
    type: governance
    scope: all_deployments
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: cross_chain_bridge
    type: bridge
    scope: [bnb, base]
    assets: [LBTC]
active_risks:
  - risk_id: restaking_protocol_dep
    deployment: all_deployments
    note: "LBTC backing relies on Babylon Protocol BTC staking scripts — novel mechanism with limited track record; slashing conditions may apply"
  - risk_id: bridge_dep
    deployment: [bnb, base]
    note: "LBTC on BNB and Base is bridged; bridge exploit or pause = unbacked LBTC on those chains"
  - risk_id: minter_key_leak
    deployment: all_deployments
    note: "Lombard multisig controls LBTC mint authority; key compromise enables unbacked minting"
  - risk_id: governance_hostile_decision
    deployment: all_deployments
    note: "Lombard governance can change mint parameters, operator set, and fee structure — decisions are not time-locked by a DAO"
audits:
  - firm: Multiple (12 reports)
    date: 2024-01
    url: ""
---

## Overview

Lombard LBTC is a restaked Bitcoin token backed by BTC deposited into Babylon Protocol's BTC staking scripts. LBTC holders have a claim on BTC securing Babylon's PoS chain; staking rewards accrue as additional BTC backing. The Lombard multisig controls the minting authority and protocol upgrades. LBTC is deployed on Ethereum as the primary chain and bridged to BNB and Base.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Cross-chain deployment adds a bridge risk layer:
- Ethereum: primary issuance; risk is dominated by Babylon staking conditions and Lombard multisig integrity
- BNB / Base: LBTC is bridged — bridge exploit or pause results in unbacked LBTC on those chains; each deployment may have independent bridge operators and multisig thresholds
- Babylon Protocol is an early-stage restaking system for BTC; slashing conditions, validator behaviour, and withdrawal mechanics are less battle-tested than Ethereum equivalents

## Key parameters

| Parameter | Detail |
|-----------|--------|
| BTC custody | Babylon staking scripts (not Lombard-held) |
| Mint authority | Lombard multisig |
| Oracle | Chainlink BTC/USD |
| Bridge (BNB/Base) | Proprietary cross-chain bridge |
| Audit count | 12 PDFs (lombard-finance/evm-smart-contracts/docs/audit) |
