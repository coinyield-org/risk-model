---
slug: ondo
name: Ondo Finance
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2700000000
    since: 2023-01-12
  - chain: polygon
    tvl_usd: 0
    since: 2023-06-01
    note: "Secondary deployment"
  - chain: arbitrum
    tvl_usd: 0
    since: 2023-09-01
    note: "Secondary deployment"
  - chain: solana
    tvl_usd: 0
    since: 2024-03-01
    note: "OUSG/USDY issued natively on Solana"
dependencies:
  - id: ondo_finance_inc
    type: issuer_manager
    scope: all_deployments
    note: "Ondo Finance Inc. manages fund subscriptions, redemptions, and NAV calculation; single operational counterparty"
  - id: ankura_trust
    type: legal_wrapper
    scope: all_deployments
    assets: [USDY]
    note: "Ankura Trust Company serves as indenture trustee for USDY's legal structure"
  - id: hsbc
    type: custodian
    scope: all_deployments
    assets: [USDY]
    note: "HSBC holds the US Treasuries and bank deposits backing USDY"
  - id: morgan_stanley
    type: custodian
    scope: all_deployments
    assets: [OUSG]
    note: "Morgan Stanley holds assets backing OUSG (BlackRock MMF shares)"
  - id: blackrock
    type: fund_manager
    scope: all_deployments
    assets: [OUSG]
    note: "OUSG is backed by BlackRock's iShares Short Treasury Bond ETF / MMF"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: "OUSG price feed via Chainlink; NAV updated daily"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: all
    note: "Ondo Finance Inc. is the operational manager; insolvency, regulatory shutdown, or key-person departure would halt subscriptions and redemptions for both OUSG and USDY."
  - risk_id: custodian_risk
    deployment: all
    note: "USDY assets are custodied at HSBC; OUSG shares are held via Morgan Stanley. Custodian failure or asset freeze (e.g., sanctions) would impair redemption."
  - risk_id: issuer_blacklist_function
    deployment: all
    note: "Ondo contract admin retains the ability to freeze individual addresses on OUSG and USDY. Admin key compromise or coercion enables targeted asset freeze."
  - risk_id: transfer_restriction_list
    deployment: all
    note: "Both OUSG and USDY enforce KYC whitelists; non-whitelisted addresses cannot receive or redeem tokens. Secondary market liquidity is constrained to whitelisted participants only."
  - risk_id: rwa_business_hours
    deployment: all
    note: "Redemptions require T+1 or T+2 wire settlement during US business hours. Weekend and holiday market dislocations cannot be arbitraged via on-chain mechanisms until next business day."
  - risk_id: attestation_vs_audit_gap
    deployment: all
    note: "NAV is computed daily by Ondo based on custodian statements, not real-time on-chain proof. There is no continuous cryptographic proof of reserves; users rely on periodic attestations."
  - risk_id: oracle_staleness
    deployment: all
    note: "Daily NAV updates mean the on-chain price of OUSG can be up to 24 hours stale. Protocols that accept OUSG as collateral may use an outdated valuation during a rapid rate spike."
audits:
  - firm: Cyfrin
    date: 2023-09
    url: ""
  - firm: Spearbit
    date: 2023-11
    url: ""
  - firm: Trail of Bits
    date: 2024-01
    url: ""
---

## Overview

Ondo Finance issues tokenized short-duration US Treasury products: OUSG (backed by
BlackRock MMF shares) and USDY (yield-bearing stablecoin backed by US Treasuries and
bank deposits). Tokens are KYC-gated to institutional and accredited investors. NAV is
updated daily and redemptions require wire transfers during business hours, creating
structural latency between on-chain price and real-world settlement.

## Type-specific risks

See `types/rwa.md` for base risk profile.

## Deployment divergence

Ethereum mainnet holds the vast majority of TVL. Solana OUSG/USDY are bridged via
Wormhole, adding bridge dependency and potential synchronization lag on NAV updates
relative to the Ethereum canonical deployment.

## Key parameters (ethereum, as of 2026-01)

| Product | Underlying | Custodian | Redemption | Min Investment |
|---------|-----------|-----------|------------|----------------|
| OUSG | BlackRock STBT / iShares | Morgan Stanley | T+2 business day | $100,000 |
| USDY | US Treasuries + bank deposits | HSBC | T+2 business day | $500 |
