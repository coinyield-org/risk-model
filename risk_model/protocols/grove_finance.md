---
slug: grove_finance
name: Grove Finance
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 3300000000
    since: 2024-01-01
dependencies:
  - id: morpho
    type: underlying_protocol
    scope: [ethereum]
    note: "All TVL is deployed into Morpho V1/V2 markets; Grove vaults are Morpho MetaMorpho curators"
  - id: grove_team
    type: governance
    scope: [ethereum]
    note: "Grove team acts as risk curator: selects markets, sets allocation caps, and manages vault strategy"
  - id: underlying_collateral_markets
    type: collateral
    scope: [ethereum]
    note: "Morpho market collateral assets (wstETH, WBTC, USDC, etc.) each carry independent risk profiles"
active_risks:
  - risk_id: downstream_protocol_failure
    deployment: ethereum
    note: "Grove's entire TVL is deployed into Morpho markets; a critical Morpho smart contract failure, bad debt socialization, or governance attack on Morpho directly and fully impacts Grove depositors"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "Grove team as vault curator can unilaterally reallocate TVL across Morpho markets, adjust supply caps per market, and withdraw from markets; a compromised or negligent curator decision is the primary protocol-specific risk"
  - risk_id: fallback_oracle_misconfig
    deployment: ethereum
    note: "Grove inherits oracle configurations from each Morpho market it allocates to; inconsistencies in oracle setups across markets (Chainlink vs Uniswap TWAP vs Redstone) create aggregated oracle risk that is difficult to monitor at the vault level"
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "Significant portion of Grove TVL may be mercenary capital attracted by MORPHO or curator incentives; reduction or cessation of incentive programs could trigger rapid TVL outflow, leaving remaining depositors with less diversified market exposure"
audits: []
---

## Overview

Grove Finance is a Morpho MetaMorpho vault curator — it manages yield-aggregation vaults
that deploy depositor capital across a curated selection of Morpho lending markets on Ethereum.
The Grove team acts as the risk curator, deciding which Morpho markets receive capital and at
what allocation caps. Grove does not have its own lending contracts; its risk surface is almost
entirely inherited from Morpho's underlying architecture plus the quality of the Grove team's
curation decisions. See `07_morpho` for the underlying protocol risk profile.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.
