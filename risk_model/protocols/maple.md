---
slug: maple
name: Maple Finance
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 1800000000
    since: 2021-05-01
  - chain: solana
    tvl_usd: 0
    since: 2022-06-01
    note: "Solana deployment paused after FTX contagion; effectively inactive"
dependencies:
  - id: maple_pool_delegates
    type: credit_manager
    scope: all_deployments
    note: "Pool delegates are the gatekeepers for loan approval and borrower underwriting; each pool is managed by a designated delegate"
  - id: maple_governance
    type: governance
    scope: all_deployments
    note: "MPL token holders govern protocol parameters, fee structures, and pool delegate onboarding"
  - id: pool_cover_providers
    type: first_loss_capital
    scope: all_deployments
    note: "Pool cover (junior tranche) absorbs initial losses before senior depositors are impacted"
  - id: chainlink
    type: oracle_provider
    scope: [ethereum]
    note: "Used for collateral valuation in secured pools; uncollateralized pools have no oracle dependency"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: [ethereum]
    note: "Maple's core product is undercollateralized institutional lending. Borrower default directly translates to lender losses. November 2022: Orthogonal Trading defaulted on ~$36M in Maple loans. December 2022: Auros Capital defaulted on $2.4M. These events demonstrated that credit underwriting quality is the dominant risk factor."
  - risk_id: whale_concentration
    deployment: ethereum
    note: "Maple pools typically have a small number of large institutional borrowers per pool. Default by any single large borrower can impair the entire pool. Lender-side concentration similarly means a single large LP exit can stress the pool."
  - risk_id: governance_hostile_decision
    deployment: all
    note: "Pool delegates have broad discretionary authority over loan approval within their pools. A compromised or colluding pool delegate can approve loans to affiliated or insolvent borrowers. MPL governance can also change delegate authorization and fee parameters."
  - risk_id: oracle_coverage_absence
    deployment: ethereum
    note: "Undercollateralized loan values are not tracked by any oracle. Lenders cannot observe real-time creditworthiness of borrowers; they rely entirely on pool delegate credit assessments and periodic disclosures."
  - risk_id: bad_debt_accumulation
    deployment: ethereum
    note: "Orthogonal Trading's $36M default in November 2022 demonstrated that bad debt socialization in Maple pools impairs all senior depositors in proportion to their share. The pool delegate's failure to detect Orthogonal's insolvency in advance is the canonical case study."
audits:
  - firm: Trail of Bits
    date: 2021-07
    url: ""
  - firm: Dedaub
    date: 2022-01
    url: ""
  - firm: Three Sigma
    date: 2022-10
    url: ""
---

## Overview

Maple Finance is an institutional undercollateralized lending protocol. Borrowers
(institutions, trading firms) receive USDC/USDT loans without full on-chain
collateralization, assessed by designated pool delegates. Lenders supply liquidity
and earn above-market yields in exchange for bearing credit risk. In November 2022,
Orthogonal Trading defaulted on ~$36M in Maple loans; in December 2022, Auros Capital
defaulted on $2.4M, demonstrating the acute credit risk inherent in the model.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Solana deployment was effectively halted following the FTX contagion in November 2022.
All material TVL and credit risk exposure is on Ethereum. The undercollateralized model
means the Ethereum deployment has a fundamentally different risk profile from standard
overcollateralized lending protocols.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Loan type | Undercollateralized institutional |
| Pool cover (first loss) | Variable by pool (typically 5-20% of pool size) |
| Loan duration | 30-90 day typical terms |
| Withdrawal mechanism | Withdrawal windows; not instant |
| Historical bad debt | ~$36M (Orthogonal Trading, Nov 2022) |
