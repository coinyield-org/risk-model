---
slug: pancakeswap
name: PancakeSwap AMM
types: [dex_amm, concentrated_liquidity]
deployments:
  - chain: bnb
    tvl_usd: 1500000000
    since: 2020-09-20
  - chain: ethereum
    tvl_usd: 80000000
    since: 2023-03-01
  - chain: arbitrum
    tvl_usd: 50000000
    since: 2023-05-01
  - chain: base
    tvl_usd: 40000000
    since: 2023-09-01
dependencies:
  - id: bnb_chain_validators
    type: chain_validators
    scope: [bnb]
    note: "BNB Smart Chain has only 21 active validators; high centralization relative to Ethereum"
  - id: chainlink
    type: oracle_provider
    scope: [bnb, ethereum, arbitrum, base]
    note: "Used for price references on select pools; TWAP also consumed by external protocols"
  - id: pancakeswap_governance
    type: governance
    scope: all_deployments
    note: "CAKE token governance controls fee tiers, emission schedules, and treasury allocation"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: all
    note: "CAKE governance is concentrated among early holders and the PancakeSwap team; a hostile or coordinated governance vote can alter fee parameters, redirect emissions, or pause pools with limited timelock protection"
  - risk_id: whale_coordination
    deployment: [bnb]
    note: "BNB chain validator set (21 validators) and large LP concentration in top pools; coordinated withdrawal by whale LPs can drain liquidity materially faster than organic exit"
  - risk_id: twap_window_misconfig
    deployment: [bnb, ethereum, arbitrum, base]
    note: "PancakeSwap V3 TWAP is consumed by external lending protocols; pools with low TVL have TWAP windows that are manipulable within a single block at acceptable cost on BNB chain given low gas"
  - risk_id: thin_liquidity_source_manipulation
    deployment: [bnb]
    note: "Many BNB chain token pairs have thin on-chain liquidity; Mango/Euler-style oracle manipulation via spot price impact is feasible on low-cap pairs where PancakeSwap is the primary price source"
  - risk_id: sequencer_downtime
    deployment: [bnb]
    note: "BSC uses a 21-validator PoSA model; historical downtime and the concentrated validator set create sequencer-equivalent risk for LP operations and arbitrage availability"
audits:
  - firm: PeckShield
    date: 2021-04
    url: ""
  - firm: PeckShield
    date: 2021-09
    url: ""
  - firm: PeckShield
    date: 2022-03
    url: ""
  - firm: PeckShield
    date: 2022-07
    url: ""
  - firm: PeckShield
    date: 2022-11
    url: ""
  - firm: PeckShield
    date: 2023-02
    url: ""
  - firm: PeckShield
    date: 2023-06
    url: ""
  - firm: PeckShield
    date: 2023-10
    url: ""
  - firm: PeckShield
    date: 2024-01
    url: ""
  - firm: Cyfrin
    date: 2024-03
    url: ""
---

## Overview

PancakeSwap is a multi-chain AMM and concentrated liquidity DEX, originally built on BNB Smart
Chain and subsequently deployed to Ethereum, Arbitrum, Base, and others. It operates both a V2
constant-product pool (dex_amm) and a V3 concentrated liquidity model (Uniswap V3 fork).
CAKE token governance controls emission schedules, fee tiers, and protocol treasury.

## Type-specific risks

See `types/dex_amm.md` and `types/concentrated_liquidity.md` for base risk profiles.

## Deployment divergence

BNB chain is the dominant deployment by TVL (~88% of total). BSC's 21-validator PoSA consensus
creates sequencer-equivalent centralization risk not present on Ethereum or Arbitrum deployments.
TWAP oracle manipulation cost is substantially lower on BNB chain due to low gas and thin liquidity
on long-tail pairs. Ethereum and L2 deployments inherit standard sequencer/bridge risks for their
respective chains.

## Key parameters (bnb, as of 2026-01)

| Pool tier | Fee | Tick spacing | Primary use |
|-----------|-----|--------------|-------------|
| V3 0.01% | 0.01% | 1 | Stablecoin pairs |
| V3 0.05% | 0.05% | 10 | Correlated pairs |
| V3 0.25% | 0.25% | 50 | Standard pairs |
| V3 1% | 1% | 200 | Exotic/volatile pairs |
