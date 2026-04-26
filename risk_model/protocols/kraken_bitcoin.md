---
slug: kraken_bitcoin
name: Kraken Bitcoin (kBTC)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 320000000
    since: 2024-01-01
    note: "kBTC is Kraken's custodial wrapped BTC product for EVM chains"
dependencies:
  - id: kraken_exchange
    type: custodian
    scope: all_deployments
    note: "Kraken exchange holds all underlying BTC in custody; kBTC is a liability of Kraken against BTC reserves held on the exchange"
  - id: kraken_team
    type: governance
    scope: all_deployments
    note: "Kraken controls the kBTC mint/burn mechanism, smart contract upgrade authority, and BTC reserve management"
active_risks:
  - risk_id: custodian_risk
    deployment: ethereum
    note: "Kraken is the sole custodian of all BTC backing kBTC; exchange insolvency, regulatory seizure (Kraken has faced significant SEC enforcement action), or operational failure would result in direct loss of the BTC backing with no on-chain recourse — identical structural risk to WBTC/cbBTC custodial model"
  - risk_id: issuer_corporate_risk
    deployment: ethereum
    note: "Kraken has been a target of SEC enforcement proceedings and operates in a heavily scrutinized regulatory environment; adverse regulatory action against Kraken — including exchange suspension, asset freeze, or forced shutdown — would directly impair kBTC's redeemability and peg"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "No public smart contract audit has been identified for kBTC; the mint/burn authority and upgrade keys held by Kraken represent an unverified attack surface — a key compromise at Kraken's infrastructure level could allow unauthorized kBTC minting"
  - risk_id: bridge_lock_backing_loss
    deployment: ethereum
    note: "kBTC is a custodial wrapped token; the backing BTC is held entirely off-chain by Kraken. A discrepancy between circulating kBTC supply and Kraken's actual BTC reserves — whether from misappropriation or operational error — directly destroys the peg with no on-chain mechanism to detect or correct it"
audits: []
---

## Overview

Kraken Bitcoin (kBTC) is Kraken exchange's custodial wrapped BTC product, allowing BTC
holders to use their assets in Ethereum DeFi. All backing BTC is held by Kraken in
centralized custody with no on-chain enforceability — the model is identical to WBTC
(BitGo custody) and cbBTC (Coinbase custody). Kraken's significant regulatory history
with the SEC and the absence of public smart contract audits make kBTC's risk profile
materially higher than comparable custodial wrapped BTC products with established audit
trails.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Custodian | Kraken exchange (sole) |
| On-chain enforceability | None — BTC is off-chain |
| Audit coverage | None identified |
| Regulatory exposure | SEC enforcement history; ongoing scrutiny |
| Reserve attestation | Not publicly confirmed |
