---
slug: quickswap
name: Quickswap DEX
types: [dex_amm, concentrated_liquidity]
deployments:
  - chain: polygon
    tvl_usd: 480000000
    since: 2020-10-01
  - chain: polygon
    tvl_usd: 0
    since: 2023-03-27
    note: "Polygon zkEVM deployment; separate chain with different security model"
dependencies:
  - id: algebra_amm
    type: underlying_protocol
    scope: [polygon]
    note: "Quickswap V3 is built on the Algebra AMM engine for concentrated liquidity; Algebra code vulnerabilities propagate directly to Quickswap"
  - id: quick_governance
    type: governance
    scope: all_deployments
    note: "QUICK token governance controls fee tiers, emission schedules, and treasury allocation"
  - id: polygon_pos_validators
    type: validator_set
    scope: [polygon]
    note: "~100 Polygon PoS validators; sidechain security model distinct from Ethereum mainnet"
  - id: chainlink
    type: oracle_provider
    scope: [polygon]
    note: "Chainlink Polygon feeds consumed by some Quickswap pools and downstream lending protocols"
active_risks:
  - risk_id: concentrated_pool_dependency
    deployment: polygon
    note: "Quickswap V3 uses Algebra AMM as its underlying concentrated liquidity engine. A critical vulnerability in Algebra contracts would affect all Quickswap V3 pools simultaneously and is outside Quickswap's direct audit and remediation scope"
  - risk_id: thin_liquidity_source_manipulation
    deployment: polygon
    note: "Many Polygon token pairs have thin on-chain liquidity with Quickswap as the primary DEX. Mango/Euler-style spot price manipulation is feasible for long-tail tokens where Quickswap TWAP feeds into external lending protocols"
  - risk_id: twap_window_misconfig
    deployment: polygon
    note: "Quickswap TWAP is consumed as a price oracle by several Polygon lending protocols. Low-TVL pools have manipulable TWAP windows, particularly during low-gas periods on Polygon PoS where manipulation cost is reduced"
  - risk_id: per_deployment_divergence
    deployment: polygon
    note: "Polygon PoS uses a ~100-validator checkpoint model (sidechain security) that is substantially less secure than Ethereum. Polygon zkEVM uses a different prover-based security model. Each deployment has a distinct risk profile that must be assessed independently"
audits:
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2021-09
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2022-01
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2022-06
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2022-11
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2023-03
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2023-08
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2024-01
    url: ""
  - firm: Algebra (via cryptoalgebra/Algebra/audits)
    date: 2024-06
    url: ""
---

## Overview

Quickswap is the dominant DEX on Polygon PoS, combining a V2 constant-product AMM
with a V3 concentrated liquidity layer built on the Algebra AMM engine. It is also
deployed on Polygon zkEVM. QUICK token governance controls fee tiers and emission
schedules. Quickswap TWAP feeds are consumed as price oracles by several Polygon
lending protocols, making it an implicit oracle provider for the Polygon DeFi ecosystem.

## Type-specific risks

See `types/dex_amm.md` and `types/concentrated_liquidity.md` for base risk profiles.

## Deployment divergence

Polygon PoS deployment (~88% of TVL) operates under sidechain security: ~100
validators checkpoint Ethereum every ~30 minutes with a 2/3 supermajority threshold.
This is materially weaker than Ethereum consensus and introduces a distinct trust
model relative to L2 deployments (Base, Optimism). Polygon zkEVM deployment relies
on a validity proof (ZK) security model with a centralized prover and separate
upgrade authority. Analysts must treat these as separate risk objects.

## Key parameters (polygon, as of 2026-01)

| Pool type | Fee range | Engine | Primary use |
|-----------|-----------|--------|-------------|
| V2 pairs | 0.3% fixed | Constant product | Long-tail tokens |
| V3 concentrated | 0.01%–1% | Algebra AMM | MATIC/stablecoin pairs |
| Polygon validators | ~100 | PoS checkpoint | Chain security |
| TWAP consumers | Multiple lending protocols | Quickswap V2/V3 | Oracle source |
