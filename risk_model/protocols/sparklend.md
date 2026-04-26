---
slug: sparklend
name: SparkLend
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 2900000000
    since: 2023-05-10
  - chain: gnosis
    tvl_usd: 0
    since: 2023-10-01
    note: "Minor deployment; majority of TVL on Ethereum mainnet"
dependencies:
  - id: makerdao_sky
    type: governance
    scope: all_deployments
    note: "SparkLend governance is fully controlled by MakerDAO/Sky DAO; all risk parameter changes require MakerDAO executive vote"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: maker_osm
    type: oracle
    scope: [ethereum]
    note: "MakerDAO Oracle Security Module (OSM) introduces 1-hour price delay for collateral feeds"
  - id: dai_usds
    type: stablecoin
    scope: all_deployments
    assets: [DAI, USDS]
    note: "Primary borrowable asset; supply depends on MakerDAO PSM capacity"
  - id: sdai
    type: yield_bearing_stablecoin
    scope: [ethereum]
    assets: [sDAI]
    note: "Accepted as collateral; yield sourced from MakerDAO DSR"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: [ethereum, gnosis]
    note: "All SparkLend risk parameters (caps, LTVs, rate strategies, asset listings) are controlled by MakerDAO governance. A hostile or miscalibrated MakerDAO executive vote can directly modify SparkLend's risk profile without SparkLend-specific safeguards."
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "SparkLend inherits MakerDAO's OSM design, which delays price feeds by 1 hour. During rapid price drops, the protocol operates on stale collateral valuations, creating a window where insolvent positions are not yet liquidatable."
  - risk_id: native_stablecoin_peg_stress
    deployment: ethereum
    note: "DAI/USDS borrowable liquidity depends entirely on MakerDAO PSM capacity. A PSM imbalance or USDS migration friction can constrain borrows and spike utilization unexpectedly."
  - risk_id: whale_concentration
    deployment: ethereum
    note: "A small number of large borrowers drive the majority of DAI/USDS demand on SparkLend; coordinated repayment or new large positions materially shifts utilization and rates."
audits:
  - firm: ChainSecurity
    date: 2023-05
    url: ""
---

## Overview

SparkLend is a lending protocol built as a fork of Aave V3, deployed and governed by
MakerDAO/Sky DAO. It serves as the primary venue for borrowing DAI and USDS against
blue-chip collateral (wstETH, wBTC, USDC, sDAI). Governance is entirely delegated to
MakerDAO, meaning risk parameter changes flow through MakerDAO executive votes rather
than a standalone SparkLend governance process.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Gnosis Chain deployment is minor by TVL. Ethereum mainnet carries ~100% of material
exposure. The OSM oracle delay is unique to SparkLend's design versus standard Aave V3
deployments and materially affects liquidation timing during fast market moves.

## Key parameters (ethereum, as of 2026-01)

| Asset | LTV | Liq Threshold | Oracle |
|-------|-----|---------------|--------|
| wstETH | 79% | 80% | MakerDAO OSM (1hr delay) |
| wBTC | 70% | 75% | MakerDAO OSM (1hr delay) |
| USDC | 77% | 80% | Chainlink USDC/USD |
| sDAI | 77% | 80% | MakerDAO DSR rate |
