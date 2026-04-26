---
slug: tether_gold
name: Tether Gold (XAUt)
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2100000000
    since: 2020-01-23
  - chain: tron
    tvl_usd: 1300000000
    since: 2020-01-23
dependencies:
  - id: tether_holdings
    type: custodian
    scope: all_deployments
    note: "Tether Holdings Ltd holds physical gold bars in Swiss vaults; sole custodian with no independent trustee"
  - id: lbma
    type: settlement
    scope: all_deployments
    note: "London Bullion Market Association provides the market for gold settlement; XAUt redemption is via LBMA-standard delivery"
  - id: bdo
    type: attestation
    scope: all_deployments
    note: "BDO provides quarterly attestation reports on gold reserves; not a full audit — scope and methodology are limited"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: [ethereum, tron]
    note: "Tether Holdings is the sole custodian of all physical gold backing XAUt; insolvency, regulatory seizure, or custodian fraud results in loss of backing with no on-chain recourse for token holders"
  - risk_id: deployer_key_leak
    deployment: [ethereum, tron]
    note: "Tether controls the mint and burn authority for XAUt on both chains; compromise of Tether's signing keys allows uncollateralized minting or blacklisting of holders"
  - risk_id: deep_chain_stablecoin
    deployment: [ethereum, tron]
    note: "Trust chain: XAUt → Tether Holdings → physical gold → Swiss vault → BDO attestation; BDO's attestation is not a full audit (scope excludes vault inspection procedures, ownership chain verification), creating an attestation-vs-audit gap"
  - risk_id: withdrawal_queue_delay
    deployment: [ethereum, tron]
    note: "Physical gold redemption requires LBMA settlement logistics; redemption is limited to business hours and minimum lot sizes (1 troy oz fine gold), with multi-day settlement windows not visible on-chain"
  - risk_id: issuer_blacklist_function
    deployment: [ethereum, tron]
    note: "Tether can freeze XAUt balances on both Ethereum and TRON at will, as with USDT; regulatory order or internal decision can render holder balances non-transferable"
audits: []
---

## Overview

Tether Gold (XAUt) is a gold-backed token issued by Tether Holdings on Ethereum and TRON.
Each XAUt represents ownership of one troy ounce of physical gold held in Swiss vaults,
allocated to specific gold bars. Tether is the sole custodian; there is no independent trustee.
Reserve attestations are provided quarterly by BDO but fall short of a full audit:
vault inspection, ownership chain, and encumbrance verification are out of scope.
Redemption for physical gold or cash is available only to verified account holders during business hours.

## Type-specific risks

See `types/rwa.md` for base risk profile.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Backing | Physical gold, LBMA-standard bars, Swiss vaults |
| Attestation provider | BDO (quarterly) |
| Min redemption | 1 troy oz (≈$3,300) |
| Redemption window | Business hours; T+2 to T+5 settlement |
| Blacklist authority | Tether Holdings |
