---
slug: morpho
name: Morpho
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 6600000000
    since: 2023-08-10
  - chain: base
    tvl_usd: 0
    since: 2024-01-01
    note: "Growing deployment; Coinbase-backed chains benefit from native liquidity"
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-03-01
    note: "Smaller deployment relative to mainnet"
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: "Per-market oracle; each market independently configures its price feed — no protocol-wide default"
  - id: steakhouse_financial
    type: risk_curator
    scope: [ethereum, base]
    note: "Steakhouse manages the largest MetaMorpho vaults by TVL"
  - id: gauntlet
    type: risk_curator
    scope: [ethereum, arbitrum]
    note: "Gauntlet operates risk-managed MetaMorpho vaults"
  - id: b_protocol
    type: risk_curator
    scope: [ethereum]
    note: "B.Protocol curates select vaults"
  - id: re7_labs
    type: risk_curator
    scope: [ethereum]
    note: "RE7 Labs curates yield-focused vaults"
  - id: underlying_collateral_issuers
    type: issuer
    scope: all_deployments
    assets: [wstETH, USDC, WBTC, cbETH]
active_risks:
  - risk_id: oracle_coverage_absence
    deployment: all_deployments
    note: "Morpho Blue markets are permissionlessly deployed; any party can create a market with a misconfigured or missing oracle. Even within curator-managed vaults, oracle misconfiguration at market creation is the primary attack surface (not Chainlink failure per se, but incorrect feed assignment)"
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "Steakhouse and Grove (B.Protocol) curate the majority of USDC/USDT Morpho TVL; curator error (wrong LTV, wrong oracle, wrong asset whitelist) propagates to all depositors in their vaults without an additional governance layer to catch it"
  - risk_id: whale_concentration
    deployment: ethereum
    note: "A small number of large liquidity providers dominate individual vault TVL; coordinated or spooked withdrawal causes immediate utilization spikes and temporarily blocks remaining depositors from withdrawing"
  - risk_id: liquidation_bonus_too_small
    deployment: all_deployments
    note: "Each Morpho market has its own LLTV and liquidation incentive set by the curator at deployment; markets with aggressive LLTVs and thin liquidation bonuses may become unprofitable to liquidate during a volatile price gap"
audits:
  - firm: Trail of Bits
    date: 2023-07
    url: ""
  - firm: Spearbit
    date: 2023-08
    url: ""
  - firm: Cantina
    date: 2023-09
    url: ""
  - firm: Certora
    date: 2023-10
    url: ""
  - firm: OpenZeppelin
    date: 2023-11
    url: ""
---

## Overview

Morpho (Morpho Blue + MetaMorpho) is a permissionless lending primitive where anyone
can create an isolated lending market by specifying a collateral asset, loan asset,
LLTV, and oracle. MetaMorpho vaults are curated aggregation layers built on top by
independent risk curators (Steakhouse, Gauntlet, RE7, B.Protocol/Grove) who allocate
depositor funds across markets. The protocol has no central risk committee — safety
depends entirely on the quality of curator market selection and oracle configuration.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Base deployment benefits from native USDC and cbETH liquidity but has shallower
liquidation depth. Arbitrum deployment is smaller with fewer active curators.
Per-deployment risk profiles can diverge significantly based on which curators
operate on each chain.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Market creation | Permissionless |
| LLTV range (typical) | 77%–98% depending on asset pair |
| Oracle requirement | Per-market; curator-defined at deployment |
| Liquidation incentive | Per-market; typically 1%–10% depending on LLTV |
| MetaMorpho vault fee | Up to 50% of yield, set per vault by curator |
| Protocol fee | 0% (governance can enable up to 25% of vault fee) |
