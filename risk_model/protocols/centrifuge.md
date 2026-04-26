---
slug: centrifuge
name: Centrifuge Protocol
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2000000000
    since: 2021-04-01
    note: "Primary user-facing chain; liquidity pools and DROP/TIN tokens issued here"
  - chain: centrifuge
    tvl_usd: 0
    since: 2021-04-01
    note: "Centrifuge Parachain (Substrate); handles NFT-based loan origination and cross-chain messaging"
dependencies:
  - id: asset_originators
    type: credit_manager
    scope: all_deployments
    note: "Each Centrifuge pool is managed by a separate asset originator (e.g., BlockTower, New Silver, Fasanara). They underwrite real-world loans and represent the primary credit risk for each pool."
  - id: makerdao
    type: liquidity_provider
    scope: [ethereum]
    note: "MakerDAO has historically been the largest single liquidity provider to Centrifuge pools via the RWA vault program; wind-down of MakerDAO RWA vaults would materially reduce TVL"
  - id: spv_legal_structures
    type: legal_wrapper
    scope: all_deployments
    note: "Each pool is backed by a separate Special Purpose Vehicle (SPV) structured in a specific jurisdiction; legal enforceability of on-chain liquidation varies by jurisdiction"
  - id: polkadot_bridge
    type: bridge
    scope: [ethereum, centrifuge]
    note: "Cross-chain messaging between Ethereum and Centrifuge Parachain via XCM and bridge relayers"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: all
    note: "Each asset originator is an independent credit risk. Originator insolvency (business failure, fraud, or legal issues) would impair the pool they manage. Historical incidents include BlockTower credit pool underperformance and New Silver pool restructuring."
  - risk_id: rwa_counterparty_default
    deployment: all
    note: "Real-world borrowers within each structured credit pool can default on their underlying loans. Unlike crypto-native collateral, recovery is subject to jurisdiction-specific insolvency law and SPV liquidation timelines, which can take months to years."
  - risk_id: attestation_vs_audit_gap
    deployment: all
    note: "NAV of each pool is computed by the asset originator based on their internal loan book valuations. There is no continuous on-chain proof of individual loan performance; lenders rely on periodic originator-provided reports."
  - risk_id: rwa_business_hours
    deployment: all
    note: "Pool redemptions are subject to lock-up periods defined per pool (often 30-90 days). Investors cannot exit on-demand; liquidity is gated by the loan repayment schedule of the underlying real-world borrowers."
  - risk_id: oracle_coverage_absence
    deployment: all
    note: "Individual loan NAV pricing is subjective and originator-reported. There is no independent on-chain oracle providing real-time loan valuations. This creates information asymmetry between originators and passive liquidity providers."
  - risk_id: fiat_ramp_gating
    deployment: all
    note: "Capital flows into and out of Centrifuge pools require fiat wire transfers and KYC processes. On-chain secondary market liquidity for pool tokens (DROP/TIN) is thin; practical exit requires waiting for underlying loan repayments."
audits:
  - firm: SR Labs
    date: 2022-07
    url: ""
  - firm: Least Authority
    date: 2022-11
    url: ""
  - firm: Kudelski Security
    date: 2023-03
    url: ""
---

## Overview

Centrifuge Protocol enables asset originators to tokenize real-world credit assets
(trade receivables, real estate loans, structured credit) and use them as collateral
for on-chain financing. Each pool is structured via an SPV and managed by an
independent originator. Liquidity providers supply DAI/USDC and receive DROP (senior,
lower yield, lower risk) or TIN (junior, higher yield, first-loss) tokens.
MakerDAO has historically been the largest LP, providing liquidity through RWA vaults.

## Type-specific risks

See `types/rwa.md` for base risk profile.

## Deployment divergence

The Centrifuge Parachain (Substrate-based) handles NFT-based loan origination and
cross-chain messaging. Ethereum is where user-facing liquidity pools and token
issuance reside. The cross-chain messaging layer between Ethereum and Centrifuge
Parachain introduces bridge dependency risk not present in Ethereum-only RWA protocols.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Pool structure | Senior (DROP) + Junior (TIN) tranches per pool |
| Typical pool lockup | 30-90 days (varies by originator) |
| NAV computation | Originator-reported; periodic (not continuous) |
| Number of active pools | ~15-25 (varies by active originator set) |
| Primary liquidity source | MakerDAO RWA vaults (historically dominant) |
