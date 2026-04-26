---
slug: wbtc
name: Wrapped BTC (WBTC)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 8900000000
    since: 2019-01-31
  - chain: arbitrum
    tvl_usd: 0
    since: 2021-09-01
    note: "Bridged from Ethereum; no separate BTC custody on Arbitrum"
  - chain: polygon
    tvl_usd: 0
    since: 2021-06-01
    note: "Bridged from Ethereum; no separate BTC custody on Polygon"
dependencies:
  - id: bitgo
    type: custodian
    scope: all_deployments
    note: "BitGo is the sole custodian holding all underlying BTC in cold storage; mint/burn requires BitGo authorization"
  - id: bit_global_dao
    type: governance
    scope: all_deployments
    note: "BiT Global DAO (Hong Kong, Justin Sun-affiliated) took over custody governance from wBTC DAO in 2024"
  - id: wbtc_merchants
    type: mint_burn_agents
    scope: all_deployments
    note: "Authorized merchants initiate mint/burn; they do not hold BTC themselves"
active_risks:
  - risk_id: custodian_risk
    deployment: ethereum
    note: "BitGo holds 100% of backing BTC in centralized custody; insolvency, seizure, or insider malfeasance at BitGo would result in direct loss of backing. The 2024 custody transfer to BiT Global (Justin Sun-affiliated entity, Hong Kong) substantially elevated this risk; several large DeFi protocols (Aave, MakerDAO) delisted or reduced WBTC exposure in response"
  - risk_id: minter_key_leak
    deployment: ethereum
    note: "The WBTC mint authority is controlled by a multisig; compromise of a threshold of signers allows unauthorized minting and subsequent backing dilution"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "BiT Global DAO controls the custodian appointment; a hostile or coerced DAO decision could replace BitGo with a less reputable custodian or redirect BTC reserves"
  - risk_id: bridge_lock_backing_loss
    deployment: [arbitrum, polygon]
    note: "WBTC on Arbitrum and Polygon is bridged ERC-20 — loss of the Ethereum-side canonical WBTC backing propagates instantly to L2 holders; there is no additional buffer"
audits:
  - firm: Chainsecurity
    date: 2019-01
    url: ""
---

## Overview

WBTC (Wrapped BTC) is an ERC-20 token pegged 1:1 to Bitcoin, backed by BTC held
in custody by BitGo. It is the dominant BTC representation in Ethereum DeFi, used
as collateral across Aave, MakerDAO, Compound, and Curve. In August 2024, custody
governance was transferred to BiT Global (a Justin Sun-affiliated Hong Kong entity),
triggering a significant trust controversy and partial delisting from major protocols.
The fundamental risk model is custodial: the entire $8.9B backing is concentrated in
a single off-chain custodian with no on-chain enforceability.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Arbitrum and Polygon deployments are bridged ERC-20 representations of Ethereum WBTC.
They inherit all custodial risks of the Ethereum token and add native bridge risk
(canonical Arbitrum and Polygon bridges) on top. There is no separate BTC custody
for these chains — backing loss on Ethereum instantly makes L2 WBTC unbacked.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Custodian | BitGo (sole) |
| Governance | BiT Global DAO (since Aug 2024) |
| BTC reserves proof | Monthly PoR attestation by BitGo |
| Mint authorization | BitGo + authorized merchants |
| On-chain enforceability | None — BTC is off-chain |
| Smart contract upgradeability | Owner-controlled; merchant whitelist mutable |
