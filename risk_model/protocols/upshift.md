---
slug: upshift
name: Upshift
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 310000000
    since: 2024-01-01
dependencies:
  - id: morpho
    type: underlying_protocol
    scope: [ethereum]
    note: "Upshift allocates capital to Morpho lending markets as part of its yield strategy"
  - id: aave
    type: underlying_protocol
    scope: [ethereum]
    note: "Upshift uses Aave V3 as one of its underlying yield sources"
  - id: pendle
    type: underlying_protocol
    scope: [ethereum]
    note: "Upshift may allocate to Pendle PT/YT positions for fixed-rate or yield-trading exposure"
  - id: upshift_team
    type: governance
    scope: [ethereum]
    note: "Upshift team acts as the capital allocator, deciding protocol allocation weights and rebalancing timing; no DAO governance identified"
active_risks:
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "Upshift's yield depends on the allocation strategy across Morpho, Aave, and Pendle; a critical failure in any of these underlying protocols — Morpho oracle manipulation, Aave governance attack, or Pendle maturity liquidity crisis — propagates directly to Upshift depositors with no independent buffer"
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "A portion of Upshift TVL may be attracted by yield boosts, MORPHO emissions, or Pendle point campaigns; when these incentive programs end, capital will likely migrate to higher-yield venues, leaving remaining depositors with reduced diversification and less favorable allocation options"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "No public audits have been identified for Upshift; the team-controlled allocation strategy and any contract upgrade authority represent an unquantified attack surface — a compromised admin key could reallocate depositor capital to malicious contracts or drain reserves"
  - risk_id: deep_chain_yield_trading
    deployment: ethereum
    note: "Upshift allocations to Pendle PT positions create multi-layer dependency chains: Upshift → Pendle → underlying yield token (e.g., rsETH) → EigenLayer → Ethereum staking; a failure at any layer of a Pendle position propagates to the Upshift vault NAV"
audits: []
---

## Overview

Upshift is an onchain capital allocator that deploys depositor funds across a curated set
of DeFi protocols on Ethereum — primarily Morpho, Aave, and Pendle — to maximize risk-adjusted
yield. The Upshift team manages allocation weights and rebalancing decisions. Unlike purely
passive vaults, Upshift's yield profile changes dynamically with its allocation decisions,
creating a dependency on both the underlying protocol health and the quality of the
Upshift team's capital allocation judgment.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.
