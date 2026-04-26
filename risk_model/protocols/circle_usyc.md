---
slug: circle_usyc
name: Circle USYC (Hashnote)
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2900000000
    since: 2023-11-01
dependencies:
  - id: hashnote
    type: fund_manager
    scope: [ethereum]
    note: "Hashnote International Short Duration Fund Ltd; asset manager for underlying short-duration US Treasuries"
  - id: circle
    type: distribution
    scope: [ethereum]
    assets: [USDC]
    note: "Circle distributes USYC via CCTP infrastructure; USDC used for subscription/redemption"
  - id: us_treasury_market
    type: underlying_asset
    scope: [ethereum]
    note: "Underlying portfolio: US T-bills and short-duration Treasuries; NAV moves with rate environment"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: ethereum
    note: "Hashnote is the asset manager; operational failure, regulatory action against Hashnote, or fund wind-down would disrupt redemptions and mark NAV to zero pending liquidation of underlying Treasuries"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "USYC NAV is updated once per business day; intraday pricing for DeFi integrations (e.g., lending collateral) relies on a daily snapshot that can diverge significantly from real-time Treasury market moves, creating stale-price collateral risk"
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "Redemptions are settled during US business hours only; outside these windows, USYC holders cannot redeem, creating an operational liquidity gap for DeFi protocols treating USYC as liquid collateral"
  - risk_id: issuer_blacklist_function
    deployment: ethereum
    note: "USYC token has transfer restriction logic; only whitelisted addresses (KYC'd institutional investors) can hold and transfer, effectively blacklisting all non-whitelisted addresses by default"
  - risk_id: deep_chain_stablecoin
    deployment: ethereum
    note: "Trust chain: USYC → Hashnote (manager) → US T-bills → Circle/CCTP (distribution) → attestation provider; no public full audit covers the complete chain — NAV attestations are periodic and limited in scope"
audits: []
---

## Overview

Circle USYC (formerly Hashnote USYC) is a tokenized short-duration US Treasury fund
distributed via Circle's infrastructure on Ethereum. Hashnote International Short Duration
Fund Ltd manages the underlying portfolio of US T-bills and repo agreements. NAV accrues
daily as interest is earned. USYC transfers are restricted to KYC-approved institutional
investors; Circle CCTP facilitates USDC-based subscription and redemption during US
business hours. No public audit of fund operations is available.

## Type-specific risks

See `types/rwa.md` for base risk profile.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Underlying assets | US T-bills, short-duration Treasuries, repo |
| Asset manager | Hashnote International Short Duration Fund Ltd |
| Distribution | Circle (CCTP / USDC) |
| NAV update frequency | Daily (business days only) |
| Eligible investors | Institutional (KYC/AML whitelisted) |
| Redemption window | US business hours; T+0 to T+1 |
