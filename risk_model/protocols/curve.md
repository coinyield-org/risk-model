---
slug: curve
name: Curve DEX
types: [dex_amm, stableswap]
deployments:
  - chain: ethereum
    tvl_usd: 1800000000
    since: 2020-01-22
  - chain: arbitrum
    tvl_usd: 0
    since: 2021-10-01
    note: "Secondary deployment; material pools (tricrypto, 2pool)"
  - chain: optimism
    tvl_usd: 0
    since: 2022-06-01
    note: "Secondary deployment"
  - chain: polygon
    tvl_usd: 0
    since: 2021-06-01
    note: "Secondary deployment"
  - chain: avalanche
    tvl_usd: 0
    since: 2021-11-01
    note: "Secondary deployment"
  - chain: base
    tvl_usd: 0
    since: 2023-09-01
    note: "Secondary deployment"
dependencies:
  - id: vecry_governance
    type: governance
    scope: all_deployments
    note: "veCRV holders control pool parameter changes (A parameter, fees) and gauge weight allocation"
  - id: convex_finance
    type: governance_concentrator
    scope: all_deployments
    note: "Convex holds ~50% of all veCRV, giving it effective governance majority; Convex governance controls Curve gauge emissions"
  - id: vyper_compiler
    type: compiler
    scope: all_deployments
    note: "Curve contracts are written in Vyper; a Vyper 0.2.15-0.3.0 reentrancy bug was exploited in July 2023 causing $73M in losses"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: all
    note: "Convex Finance holds approximately 50% of all veCRV, giving it a near-controlling vote in Curve governance. A compromised or hostile Convex governance action (e.g., via Convex's own multisig) can unilaterally redirect gauge emissions and influence pool parameter changes."
  - risk_id: readonly_reentrancy
    deployment: [ethereum, arbitrum, optimism]
    note: "In July 2023, a read-only reentrancy vulnerability in Vyper compiler versions 0.2.15-0.3.0 was exploited across multiple Curve pools, resulting in approximately $73M in total losses. Patched pools exist but the compiler-level origin means unpatched forks and integrations remain at risk."
  - risk_id: thin_liquidity_source_manipulation
    deployment: all
    note: "Many DeFi protocols use Curve pools as on-chain price oracles (TWAP or spot). Pools with relatively thin liquidity can be manipulated by large flash-loan-funded swaps, propagating incorrect prices to oracle consumers built on top of Curve."
  - risk_id: amplification_misconfig
    deployment: all
    note: "Curve pool operators can ramp the amplification coefficient (A parameter) over time. Rapid A parameter changes alter pool invariant and can be front-run to extract value from LPs during the transition window."
  - risk_id: whale_concentration
    deployment: all
    note: "veCRV is heavily concentrated. Beyond Convex (~50%), a handful of protocols and wallets control the majority of remaining veCRV. Low retail turnout in gauge votes means a small coalition can capture gauge emissions."
audits:
  - firm: Trail of Bits
    date: 2020-09
    url: ""
  - firm: Trail of Bits
    date: 2021-10
    url: ""
---

## Overview

Curve DEX is a stableswap and concentrated-liquidity AMM optimized for low-slippage
swaps between correlated assets. It is the dominant on-chain venue for stablecoin-to-
stablecoin and LST-to-ETH swaps. Governance is controlled by veCRV holders; Convex
Finance holds ~50% of veCRV, making it the de-facto governance controller. In July
2023, a Vyper compiler reentrancy bug was exploited across multiple Curve pools,
resulting in ~$73M in total losses across the ecosystem.

## Type-specific risks

See `types/dex_amm.md` and `types/stableswap.md` for base risk profile.

## Deployment divergence

L2 deployments (Arbitrum, Optimism, Base) carry additional sequencer dependency.
The July 2023 reentrancy exploit was most severe on Ethereum mainnet where pool
sizes are largest, but the underlying compiler vulnerability affected all Vyper-
compiled deployments across chains.

## Key parameters (ethereum, as of 2026-01)

| Pool | Amplification (A) | Fees | Oracle Used By |
|------|-------------------|------|----------------|
| 3pool (USDC/USDT/DAI) | 2000 | 0.01% | Widely (as reference) |
| stETH/ETH | 50 | 0.04% | Aave, Maker (TWAP) |
| crvUSD/USDT | 500 | 0.01% | crvUSD peg mechanism |
