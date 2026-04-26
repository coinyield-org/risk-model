---
slug: uniswap_v3
name: Uniswap V3
types: [dex_amm, concentrated_liquidity]
deployments:
  - chain: ethereum
    tvl_usd: 1400000000
    since: 2021-05-05
  - chain: arbitrum
    tvl_usd: 150000000
    since: 2021-08-31
  - chain: optimism
    tvl_usd: 80000000
    since: 2022-01-01
  - chain: polygon
    tvl_usd: 50000000
    since: 2021-12-22
  - chain: base
    tvl_usd: 40000000
    since: 2023-08-09
  - chain: bnb
    tvl_usd: 20000000
    since: 2023-06-01
  - chain: avalanche
    tvl_usd: 10000000
    since: 2022-11-01
dependencies:
  - id: uniswap_governance
    type: governance
    scope: all_deployments
    note: "UNI token governance controls the protocol fee switch; fee revenue is currently off but can be activated by governance vote"
  - id: twap_oracle_consumers
    type: downstream_consumers
    scope: all_deployments
    note: "Uniswap V3 TWAP is used as oracle by many external lending and derivatives protocols; manipulation risk is inherited by those consumers"
active_risks:
  - risk_id: liquidation_sandwich
    deployment: all
    note: "JIT (Just-In-Time) liquidity attacks: MEV bots add concentrated liquidity at the exact tick of a large swap in the same block, capture fees, then immediately remove — diluting organic LP returns without adding real depth. This is structurally enabled by V3's per-block LP management"
  - risk_id: twap_window_misconfig
    deployment: all
    note: "Uniswap V3 TWAP security is entirely a function of the observation window chosen by consumers. A narrow window (e.g. 5 min) is manipulable via flash-loan-funded spot moves; a wide window (e.g. 24h) is stale during fast markets. Uniswap itself does not enforce a window — risk is fully externalized"
  - risk_id: protocol_token_as_collateral_elsewhere
    deployment: [ethereum, arbitrum]
    note: "V3 LP positions are ERC-721 NFTs used as collateral in multiple lending protocols (Euler, Morpho plugins, NFT lending). Forced liquidation of LP-NFT collateral under stress creates concentrated tick removals that spike slippage for remaining traders"
  - risk_id: thin_liquidity_source_manipulation
    deployment: [bnb, avalanche, polygon]
    note: "Low-TVL pools on non-Ethereum deployments have thin liquidity relative to Uniswap V3's status as a benchmark oracle; manipulation is cheaper on these chains and the TWAP is trusted by downstream consumers as if it were mainnet-depth"
  - risk_id: governance_hostile_decision
    deployment: all
    note: "UNI governance controls the fee switch across all deployments; activation and fee-destination decisions are subject to UNI concentration risk and delegate politics, which have historically been slow and occasionally captured by large holders"
audits:
  - firm: Trail of Bits
    date: 2021-04
    url: ""
  - firm: Trail of Bits
    date: 2021-07
    url: ""
  - firm: Spearbit
    date: 2022-06
    url: ""
  - firm: Spearbit
    date: 2023-01
    url: ""
  - firm: Trail of Bits
    date: 2023-04
    url: ""
  - firm: Cyfrin
    date: 2023-08
    url: ""
  - firm: Trail of Bits
    date: 2024-01
    url: ""
  - firm: Spearbit
    date: 2024-06
    url: ""
---

## Overview

Uniswap V3 is the concentrated liquidity AMM that enables LPs to provide liquidity within
custom price ranges (ticks), achieving higher capital efficiency at the cost of active
position management. It introduced the TWAP oracle as a first-class primitive, now used
as a price source by a large number of DeFi lending and derivatives protocols. LP positions
are represented as NFTs, enabling composability but also LP-NFT collateral use cases.

## Type-specific risks

See `types/dex_amm.md` and `types/concentrated_liquidity.md` for base risk profiles.

## Deployment divergence

Ethereum mainnet holds the majority of TVL and provides the deepest liquidity for TWAP
reliability. Arbitrum deployment benefits from lower gas costs but inherits sequencer
dependency risk. BNB, Avalanche, and Polygon deployments have materially thinner liquidity,
making TWAP manipulation cheaper per unit of capital. Fee parameters and governance execution
are uniform across deployments but timelock enforcement may vary by chain executor.

## Key parameters (ethereum, as of 2026-01)

| Fee tier | Tick spacing | Typical use |
|----------|--------------|-------------|
| 0.01% | 1 | USD stablecoin pairs |
| 0.05% | 10 | Correlated pairs (ETH/stETH) |
| 0.30% | 60 | Standard volatile pairs |
| 1.00% | 200 | Exotic / high-volatility pairs |
