---
slug: uniswap_v4
name: Uniswap V4
types: [dex_amm, concentrated_liquidity]
deployments:
  - chain: ethereum
    tvl_usd: 660000000
    since: 2024-01-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-01-01
  - chain: base
    tvl_usd: 0
    since: 2024-01-01
  - chain: optimism
    tvl_usd: 0
    since: 2024-01-01
  - chain: polygon
    tvl_usd: 0
    since: 2024-01-01
dependencies:
  - id: hook_contracts
    type: user_deployed_logic
    scope: all_deployments
  - id: uni_governance
    type: governance
    scope: all_deployments
active_risks:
  - risk_id: proxy_upgrade_authority
    deployment: all_deployments
    note: "Singleton architecture concentrates all pools in one contract — the upgrade surface covers the entire protocol TVL simultaneously"
  - risk_id: oracle_staleness
    deployment: [arbitrum, optimism, base]
    note: "TWAP oracle inherited from V3 design; on L2s, sequencer downtime creates stale TWAP windows that downstream oracle consumers may not handle correctly"
  - risk_id: governance_hostile_decision
    deployment: all_deployments
    note: "UNI governance can activate the protocol fee switch, changing economics for all LPs retroactively; governance capture risk applies"
  - risk_id: thin_liquidity_source_manipulation
    deployment: all_deployments
    note: "V4 TWAP remains manipulable in low-liquidity pools — a malicious hook on a high-TVL pool can amplify manipulation impact"
audits:
  - firm: OpenZeppelin
    date: 2024-01
    url: ""
  - firm: Trail of Bits
    date: 2024-01
    url: ""
  - firm: ABDK
    date: 2024-01
    url: ""
  - firm: Spearbit
    date: 2024-01
    url: ""
  - firm: Certora
    date: 2024-01
    url: ""
  - firm: Cyfrin
    date: 2024-01
    url: ""
  - firm: Pashov Audit Group
    date: 2024-01
    url: ""
  - firm: Codearena
    date: 2024-01
    url: ""
  - firm: Trail of Bits (periphery)
    date: 2024-06
    url: ""
---

## Overview

Uniswap V4 is a concentrated liquidity AMM deploying a singleton architecture where all pools live in a single contract. The primary innovation is the hook system: each pool can attach an arbitrary user-deployed hook contract that executes logic at swap, mint, and burn events. V4 is deployed across Ethereum, Arbitrum, Base, Optimism, and Polygon.

## Type-specific risks

See `types/dex_amm.md` and `types/concentrated_liquidity.md` for base risk profiles.

## Deployment divergence

L2 deployments inherit sequencer-specific surface:
- Arbitrum / Optimism / Base: sequencer downtime creates stale TWAP windows; protocols using V4 TWAP as an oracle may consume stale data without a sequencer uptime check
- Polygon: different finality model; reorg risk is non-zero for shallow confirmations

Hook contracts are the primary V4-specific attack surface across all deployments:
- Each pool can attach an arbitrary logic contract deployed by anyone — a malicious or buggy hook on a widely-used pool can drain that pool's liquidity or manipulate swap output
- Hook risk is not bounded by the core V4 audit surface; every new hook is an independent unaudited codebase from the perspective of users who interact with it
- High-TVL pools with popular hooks (e.g., TWAMM, dynamic fees, MEV hooks) accumulate concentrated hook risk that did not exist in V3

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Architecture | Singleton (all pools in one contract) |
| Hook system | Arbitrary user-deployed contracts per pool |
| TWAP oracle | Inherited from V3 design (manipulable in thin pools) |
| Fee switch | UNI governance-controlled, currently inactive |
| Audits | 9 reports (v4-core, v4-periphery, Trail of Bits) |
