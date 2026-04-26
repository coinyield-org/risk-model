---
slug: frax
name: Frax Finance
types: [cdp, lending]
deployments:
  - chain: ethereum
    tvl_usd: 1100000000
    since: 2020-12-31
  - chain: arbitrum
    tvl_usd: 150000000
    since: 2022-03-01
  - chain: optimism
    tvl_usd: 80000000
    since: 2022-06-01
  - chain: polygon
    tvl_usd: 40000000
    since: 2022-09-01
  - chain: base
    tvl_usd: 30000000
    since: 2023-08-01
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: curve
    type: dex_amm
    scope: [ethereum, arbitrum]
    assets: [sFRAX, frxETH/FRAX]
  - id: frxeth
    type: staking_protocol
    scope: [ethereum]
    assets: [frxETH, sfrxETH]
  - id: fxs_governance
    type: governance_token
    scope: all_deployments
active_risks:
  - risk_id: governance_hostile_decision
    deployment: all_deployments
    note: "FXS governance concentration — top holders can push parameter changes including collateral ratio, fee parameters, and new FRAX minting"
  - risk_id: concentrated_pool_dependency
    deployment: [ethereum, arbitrum]
    note: "Curve pools are critical for FRAX peg maintenance; sFRAX and frxETH/FRAX pools represent primary liquidity venue"
  - risk_id: thin_liquidity_source_manipulation
    deployment: [ethereum]
    note: "frxETH liquidity concentrated in Curve; thin secondary markets increase depeg risk under stress"
  - risk_id: native_stablecoin_peg_stress
    deployment: all_deployments
    note: "FRAX partial algorithmic history (pre-v3 FXS burn/mint) creates legacy perception risk; peg mechanism complexity reduces market confidence during stress"
  - risk_id: whale_concentration
    deployment: all_deployments
    note: "FXS token distribution is concentrated among early investors and team; governance attack surface via delegation accumulation"
audits:
  - firm: Trail of Bits
    date: 2023-04
    url: ""
  - firm: Trail of Bits
    date: 2023-09
    url: ""
  - firm: PeckShield
    date: 2023-11
    url: ""
---

## Overview

Frax Finance is a hybrid CDP and lending protocol combining FRAX (stablecoin),
frxETH (liquid staked ETH), FraxLend (permissionless lending pairs), and sFRAX
(yield-bearing FRAX vault). Originally partially algorithmic, Frax v3 moved to
full collateralization. FXS token holders govern protocol parameters including
collateral ratios and fee structures. Total TVL is approximately $1.4B.

## Type-specific risks

See `types/cdp.md` and `types/lending.md` for base risk profiles.

## Deployment divergence

Ethereum is the primary deployment with full functionality (FRAX minting, frxETH,
FraxLend, sFRAX). L2 deployments (Arbitrum, Optimism, Polygon, Base) offer
bridged FRAX and limited FraxLend functionality. Each L2 deployment introduces:
- Bridge dependency for FRAX canonical bridging
- Thinner liquidity relative to mainnet Curve pools
- Different governance execution path (L2 executor multisig)

## Key parameters (ethereum, as of 2026-01)

| Component | Collateral | Mechanism | Oracle |
|-----------|-----------|-----------|--------|
| FRAX | USDC + FXS (v3: 100% USDC) | Mint/redeem 1:1 | Chainlink USDC/USD |
| frxETH | ETH | 1:1 mint, validator-staked | Chainlink ETH/USD |
| FraxLend | Various (per pair) | Permissionless pairs | Chainlink per asset |
| sFRAX | FRAX | Yield from T-bill RWA | N/A (exchange rate) |
