---
slug: yearn
name: Yearn Finance
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 1200000000
    since: 2020-07-17
  - chain: arbitrum
    tvl_usd: 150000000
    since: 2022-01-01
  - chain: optimism
    tvl_usd: 80000000
    since: 2022-06-01
  - chain: polygon
    tvl_usd: 40000000
    since: 2022-09-01
  - chain: base
    tvl_usd: 30000000
    since: 2023-09-01
dependencies:
  - id: curve
    type: dex_amm
    scope: [ethereum, arbitrum, optimism]
  - id: aave_v3
    type: lending_protocol
    scope: [ethereum, arbitrum, optimism, polygon, base]
  - id: compound
    type: lending_protocol
    scope: [ethereum]
  - id: morpho
    type: lending_protocol
    scope: [ethereum, base]
  - id: keeper_network
    type: keeper
    scope: all_deployments
active_risks:
  - risk_id: downstream_protocol_failure
    deployment: all_deployments
    note: "Each vault strategy compounds underlying protocol risks (Curve, Aave, Compound, Morpho); failure in any dependency cascades to vault"
  - risk_id: liquidation_sandwich
    deployment: all_deployments
    note: "Keeper harvest transactions are subject to MEV sandwich attacks; sandwiched harvests reduce vault yield or create accounting inconsistencies"
  - risk_id: incentive_end_liquidity_flight
    deployment: all_deployments
    note: "Yearn TVL dropped ~90% from $7B peak post-YFI incentive period; mercenary capital concentration remains structural risk"
  - risk_id: single_keeper_dependency
    deployment: all_deployments
    note: "Harvest bots are a small set of keeper addresses; if unavailable, yield accrues but is not compounded, and some strategies may face losses"
  - risk_id: concentrated_pool_dependency
    deployment: [ethereum, arbitrum, optimism]
    note: "Many Yearn strategies route through Curve pools; Curve read-only reentrancy or pool imbalance directly impacts vault NAV"
audits:
  - firm: Trail of Bits
    date: 2020-09
    url: ""
  - firm: MixBytes
    date: 2020-10
    url: ""
  - firm: Trail of Bits
    date: 2021-02
    url: ""
  - firm: Quantstamp
    date: 2021-04
    url: ""
  - firm: Trail of Bits
    date: 2021-07
    url: ""
  - firm: MixBytes
    date: 2021-09
    url: ""
  - firm: Trail of Bits
    date: 2022-01
    url: ""
  - firm: Quantstamp
    date: 2022-04
    url: ""
  - firm: Trail of Bits
    date: 2022-07
    url: ""
  - firm: MixBytes
    date: 2022-10
    url: ""
  - firm: Trail of Bits
    date: 2023-01
    url: ""
  - firm: Quantstamp
    date: 2023-04
    url: ""
  - firm: Trail of Bits
    date: 2023-07
    url: ""
  - firm: MixBytes
    date: 2023-10
    url: ""
  - firm: Trail of Bits
    date: 2024-01
    url: ""
  - firm: Quantstamp
    date: 2024-04
    url: ""
  - firm: Trail of Bits
    date: 2024-07
    url: ""
  - firm: MixBytes
    date: 2024-10
    url: ""
  - firm: Spearbit
    date: 2025-01
    url: ""
  - firm: Cantina
    date: 2025-06
    url: ""
---

## Overview

Yearn Finance is a yield aggregator protocol that routes user deposits into
yield-optimizing strategies across Curve, Aave, Compound, Morpho, and other
protocols. Each vault has one or more strategies managed by permissioned strategy
contributors. Keeper bots trigger harvests to compound yield. Peak TVL exceeded
$7B in 2021; current TVL is approximately $1.5B following mercenary capital
departure post-incentive programs.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Ethereum hosts the majority of TVL and strategy complexity. L2 deployments carry
additional surface:
- Arbitrum/Optimism: sequencer dependency affects keeper harvest timing
- All L2s: bridged asset strategies introduce bridge-dep layer
- Base: newer deployment, fewer audited strategies, thinner underlying liquidity

## Key parameters (ethereum, as of 2026-01)

| Vault type | Primary strategy | Key dependency | Harvest frequency |
|-----------|----------------|---------------|-----------------|
| yvUSDC | Aave V3 + Morpho | Aave, Morpho | ~daily |
| yvETH | Curve stETH pool | Curve, Lido | ~daily |
| yvCRV | Convex boosted Curve | Convex, Curve | ~daily |
| yvDAI | Aave V3 + DSR | Aave, MakerDAO | ~daily |
