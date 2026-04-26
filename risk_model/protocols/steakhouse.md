---
slug: steakhouse
name: Steakhouse Financial
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 1700000000
    since: 2023-11-01
dependencies:
  - id: morpho
    type: primary_protocol
    scope: all_deployments
    note: "All Steakhouse vaults are Morpho MetaMorpho vaults; Steakhouse acts as risk curator, not contract owner"
  - id: steakhouse_team
    type: risk_curator
    scope: all_deployments
    note: "Steakhouse team makes allocation decisions across Morpho markets (collateral selection, caps, LTV)"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: "Inherited from underlying Morpho market configs for USDC, wstETH, WBTC markets"
active_risks:
  - risk_id: downstream_protocol_failure
    deployment: ethereum
    note: "100% of TVL is deployed into Morpho markets; a systemic Morpho exploit or governance failure collapses all Steakhouse vault value with no independent fallback"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "Steakhouse team controls vault strategy: market selection, supply caps, and collateral allocation. A miscalibrated or adversarial allocation decision directly reallocates depositor funds into higher-risk Morpho markets"
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "A significant portion of TVL is incentive-driven (MORPHO emissions, partner rewards); reduction or cessation of emissions risks rapid TVL withdrawal, impacting utilization and withdrawable liquidity for remaining depositors"
  - risk_id: fallback_oracle_misconfig
    deployment: ethereum
    note: "Oracle configs are inherited from individual Morpho market deployments; Steakhouse curators must verify each market's oracle setup at allocation time — misconfigs in newly listed markets are an inherited attack surface"
audits: []
---

## Overview

Steakhouse Financial operates as a risk curator for Morpho MetaMorpho vaults on Ethereum.
Depositors supply assets (primarily USDC) into Steakhouse-managed vaults, which automatically
allocate across a curated set of Morpho lending markets based on Steakhouse's risk assessments.
Steakhouse holds no protocol contracts of its own; all smart contract risk belongs to Morpho.
The curator's value-add is active market selection and cap management.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Single Ethereum deployment. No multi-chain surface; all risk is concentrated in the Morpho
mainnet deployment and Steakhouse's curator decisions on that deployment.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Vault standard | Morpho MetaMorpho (ERC-4626) |
| Primary asset | USDC |
| Collateral markets | wstETH, WBTC, USDC (blue-chip focus) |
| Curator | Steakhouse Financial team |
| Curator control | Market allocation, supply caps per market |
