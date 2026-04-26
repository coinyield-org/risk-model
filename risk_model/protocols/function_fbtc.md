---
slug: function_fbtc
name: Function FBTC
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 850000000
    since: 2024-01-01
  - chain: bnb
    tvl_usd: 0
    since: 2024-01-01
  - chain: base
    tvl_usd: 0
    since: 2024-01-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-01-01
  - chain: mantle
    tvl_usd: 0
    since: 2024-01-01
dependencies:
  - id: function_team
    type: custodian
    scope: all_deployments
  - id: btc_custodians
    type: custodian
    scope: all_deployments
  - id: multi_chain_bridge_infra
    type: bridge
    scope: [bnb, base, arbitrum, mantle]
active_risks:
  - risk_id: bridge_dep
    deployment: [bnb, base, arbitrum, mantle]
    note: "FBTC on L2s is backed by a cross-chain bridge; bridge pause or exploit = unbacked FBTC"
  - risk_id: minter_key_leak
    deployment: all_deployments
    note: "Function team controls mint authority; compromise of multisig keys allows unbacked FBTC minting"
  - risk_id: per_deployment_divergence
    deployment: [bnb, base, arbitrum, mantle]
    note: "Each chain has a separate bridge and custodian arrangement — risk profiles diverge across deployments"
audits: []
---

## Overview

Function FBTC is a wrapped Bitcoin product deployed across multiple chains. BTC is custodied by the Function team and partner BTC custodians; FBTC tokens represent a 1:1 claim on the underlying BTC. The token is bridged cross-chain via dedicated bridge infrastructure, making each non-Ethereum deployment dependent on an additional bridge layer.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Multi-chain deployment creates distinct risk layers per chain:
- Ethereum: primary issuance chain — risk is dominated by custodian and mint-key integrity
- BNB / Base / Arbitrum / Mantle: FBTC is bridged, adding a bridge exploit or pause surface on top of custodian risk; each chain may have different bridge operators, multisig thresholds, and upgrade authority
- BTC backing cannot be verified on-chain in real time — proof of reserves relies on off-chain attestations from custodians

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Custody model | Function team + BTC custodian partners |
| Mint authority | Function multisig (chain-specific) |
| Bridge mechanism | Multi-chain proprietary bridge infra |
| BTC proof of reserves | Off-chain attestation |
