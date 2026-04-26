---
slug: spark_liquidity
name: Spark Liquidity Layer
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 2200000000
    since: 2024-01-01
    note: "Onchain capital allocator routing liquidity from Sky/MakerDAO to external yield venues"
dependencies:
  - id: makerdao_sky
    type: governance
    scope: all_deployments
    note: "MakerDAO/Sky DAO controls all allocation strategy decisions for the Spark Liquidity Layer"
  - id: sparklend
    type: yield_venue
    scope: [ethereum]
    note: "SparkLend is the primary allocation destination"
  - id: aave_v3
    type: yield_venue
    scope: [ethereum]
    note: "Secondary allocation destination for idle capital"
  - id: morpho
    type: yield_venue
    scope: [ethereum]
    note: "Morpho curated markets used as additional allocation target"
active_risks:
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "The Spark Liquidity Layer allocates predominantly to SparkLend and Morpho markets. A failure, exploit, or bank run at either primary venue would directly impair the aggregator's capital and NAV."
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "All allocation decisions (which venues receive capital, in what proportion, and on what terms) are controlled by MakerDAO governance. A miscalibrated or hostile executive vote can direct capital into undercollateralized or exploited venues."
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "Allocations to external venues may be subsidized by emission incentives. When incentives end, the marginal yield advantage disappears and capital may exit rapidly, creating cascade pressure on the underlying venues."
audits: []
---

## Overview

The Spark Liquidity Layer is an onchain capital allocator operated under MakerDAO/Sky
governance. It routes surplus DAI/USDS from the Sky protocol into yield-bearing venues
including SparkLend, Aave V3, and Morpho curated markets. Allocation decisions are
governed by MakerDAO executive votes. The layer itself holds no user deposits directly;
TVL reflects the capital deployed into underlying protocols on behalf of the Sky
ecosystem.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.
