---
slug: binance_btc
name: Binance Bitcoin (BBTC)
types: [bridge]
deployments:
  - chain: bnb
    tvl_usd: 5200000000
    since: 2019-09-01
dependencies:
  - id: binance_exchange
    type: custodian
    scope: all_deployments
    note: "Sole custodian — holds all backing BTC in Binance-controlled wallets"
  - id: binance_pos_validators
    type: validator_set
    scope: [bnb]
    note: "BNB Chain validator set; Binance-aligned super validators"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: bnb
    note: "Binance is the sole custodian of all backing BTC; exchange insolvency, hack, or regulatory seizure extinguishes BBTC backing entirely"
  - risk_id: deployer_key_leak
    deployment: bnb
    note: "Binance controls mint/burn authority; compromise of Binance's signing infrastructure allows uncollateralized minting or permanent lock of supply"
  - risk_id: bridged_backing_loss
    deployment: bnb
    note: "BBTC supply is only as good as Binance's real-time BTC reserves; no on-chain proof-of-reserve; users rely on Binance attestations"
  - risk_id: deep_chain_stablecoin
    deployment: bnb
    note: "Backing chain: BBTC → Binance exchange → Bitcoin network → Binance custody ops → regulatory standing; each layer is opaque"
audits: []
---

## Overview

Binance Bitcoin (BBTC) is a custodially-wrapped BTC token issued on BNB Chain by Binance.
Each BBTC is nominally backed 1:1 by BTC held in Binance's exchange wallets.
Minting and redemption are gated through Binance's centralized KYC/AML process.
There is no smart-contract-enforced proof-of-reserve; trust is entirely placed in Binance as custodian and issuer.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Key parameters

| Parameter | Value |
|-----------|-------|
| Custodian | Binance (centralized, single entity) |
| Proof of reserve | None on-chain; periodic Binance attestations only |
| Mint/burn gating | KYC'd Binance account required |
| Redemption | Via Binance withdrawal; subject to exchange withdrawal limits |
