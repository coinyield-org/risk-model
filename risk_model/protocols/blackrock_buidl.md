---
slug: blackrock_buidl
name: BlackRock BUIDL
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2400000000
    since: 2024-03-20
    note: "Primary deployment; largest share of TVL"
  - chain: avalanche
    tvl_usd: 200000000
    since: 2024-07-01
  - chain: polygon
    tvl_usd: 150000000
    since: 2024-07-01
  - chain: arbitrum
    tvl_usd: 150000000
    since: 2024-07-01
  - chain: optimism
    tvl_usd: 100000000
    since: 2024-07-01
dependencies:
  - id: blackrock
    type: fund_manager
    scope: all_deployments
    note: "BlackRock manages the underlying USD Institutional Digital Liquidity Fund (UIDLF); investment decisions and fund operations"
  - id: bny_mellon
    type: custodian
    scope: all_deployments
    note: "BNY Mellon is the fund custodian and administrator for underlying US Treasury holdings"
  - id: securitize
    type: tokenization_platform
    scope: all_deployments
    note: "Securitize handles tokenization, whitelisting (KYC/AML), and transfer agent functions; controls token registry"
  - id: circle
    type: issuer
    scope: all_deployments
    assets: [USDC]
    note: "USDC used for T+0 subscription/redemption via Securitize API"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: all_deployments
    note: "BlackRock's underlying fund invests in US Treasuries and repo; fund NAV is exposed to Treasury market dislocations, though counterparty risk to the US government is considered remote — operational risk at BlackRock or BNY Mellon level is more material"
  - risk_id: issuer_blacklist_function
    deployment: all_deployments
    note: "Securitize as transfer agent can blacklist any address from the BUIDL token registry; regulatory order or Securitize operational failure renders affected tokens non-transferable, trapping capital"
  - risk_id: withdrawal_queue_delay
    deployment: all_deployments
    note: "T+0 redemption via Circle USDC is available only during US business hours through the Securitize API; outside these windows redemptions queue, creating an operational liquidity gap for protocols using BUIDL as collateral"
  - risk_id: deep_chain_stablecoin
    deployment: all_deployments
    note: "Trust chain: BUIDL → BlackRock → BNY Mellon custody → US Treasuries → Securitize registry → Circle USDC; public audit of the full chain is not available — institutional reporting only, not equivalent to on-chain verifiability"
  - risk_id: per_deployment_divergence
    deployment: [avalanche, polygon, arbitrum, optimism]
    note: "Non-Ethereum deployments hold BUIDL via bridge mechanisms; token transfer restrictions and whitelisting are enforced separately on each chain by Securitize, creating per-chain compliance and operational risk"
audits: []
---

## Overview

BlackRock BUIDL (USD Institutional Digital Liquidity Fund) is a tokenized money-market fund
investing in US Treasuries and overnight repo, issued on multiple chains via Securitize's
tokenization platform. Shares are represented as ERC-20 tokens but are restricted to
KYC-approved institutional investors whitelisted by Securitize. T+0 redemption for USDC
is available during US business hours via Circle. BNY Mellon holds the underlying assets.
No public audit is available; reporting follows institutional fund disclosure standards.

## Type-specific risks

See `types/rwa.md` for base risk profile.

## Deployment divergence

Ethereum is the primary deployment with the largest TVL share. Non-Ethereum deployments
(Avalanche, Polygon, Arbitrum, Optimism) hold BUIDL via chain-specific bridge mechanisms;
whitelist enforcement is replicated per-chain by Securitize, creating independent compliance
surfaces. A bridge failure on a non-Ethereum chain could disconnect local BUIDL from the
underlying fund without affecting Ethereum holders.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Underlying assets | US Treasuries, overnight repo |
| Fund custodian | BNY Mellon |
| Transfer agent / tokenizer | Securitize |
| Eligible investors | Institutional (whitelisted only) |
| Min subscription | $5,000,000 (institutional) |
| Redemption | T+0 via Circle USDC (business hours) |
