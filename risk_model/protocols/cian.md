---
slug: cian
name: CIAN Yield Layer
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 180000000
    since: 2023-01-01
  - chain: arbitrum
    tvl_usd: 120000000
    since: 2023-06-01
  - chain: avalanche
    tvl_usd: 60000000
    since: 2023-09-01
dependencies:
  - id: aave
    type: underlying_protocol
    scope: [ethereum, arbitrum]
    note: "CIAN strategies use Aave V3 as the lending layer for leveraged LST/LRT positions"
  - id: lido
    type: staking_protocol
    scope: [ethereum, arbitrum]
    assets: [stETH, wstETH]
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    note: "Some CIAN strategies include EigenLayer restaking as a yield-enhancement layer"
  - id: cian_team
    type: governance
    scope: all_deployments
    note: "Strategy operators and automation bots are controlled by the CIAN team; no public DAO or governance forum identified"
  - id: keeper_bots
    type: automation
    scope: all_deployments
    note: "Automated keeper bots execute rebalancing, leverage adjustment, and collateral management on behalf of strategy vaults"
active_risks:
  - risk_id: deep_chain_yield_trading
    deployment: [ethereum, arbitrum]
    note: "CIAN's leveraged LST/LRT strategies create 3-4 layer dependency chains: Ethereum → Lido/EigenLayer → LRT protocol → CIAN strategy → Aave leverage; each layer carries independent smart contract, slashing, and liquidation risk that compounds with leverage"
  - risk_id: single_keeper_dependency
    deployment: all
    note: "Automated strategy execution (rebalancing, deleveraging during market stress) depends on CIAN's keeper bot infrastructure; if keeper bots fail during a rapid price move, leveraged positions may breach liquidation thresholds before manual intervention is possible"
  - risk_id: incentive_end_liquidity_flight
    deployment: all
    note: "A material portion of CIAN TVL is driven by point-farming campaigns from EigenLayer and LRT protocols; cessation of these campaigns is likely to trigger rapid capital exit, leaving remaining depositors with residual exposure in illiquid or partially unwound positions"
  - risk_id: deployer_key_leak
    deployment: all
    note: "No public audits have been identified for CIAN smart contracts; strategy vault upgrade authority and admin controls represent an unquantified attack surface — a compromised admin key could redirect depositor assets or disable deleveraging mechanisms"
audits: []
---

## Overview

CIAN Yield Layer is a DeFi automation protocol that creates and manages leveraged yield
strategies, primarily targeting LST and LRT assets on Ethereum, Arbitrum, and Avalanche.
CIAN vaults automatically apply leverage against Aave lending markets to amplify staking
and restaking yields. Automated keeper bots manage collateral ratios and execute
rebalancing when positions approach liquidation thresholds. The protocol has no public
audits and its risk profile is compounded by the depth of its underlying dependency stack.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.

## Deployment divergence

Ethereum deployment carries the highest TVL and deepest strategy complexity, including
EigenLayer restaking exposure. Arbitrum deployment adds sequencer dependency risk to
keeper bot execution timing. Avalanche deployment targets different yield sources with
different liquidity profiles.
