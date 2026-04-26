---
slug: eigenlayer
name: EigenLayer
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 9800000000
    since: 2023-06-14
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
    note: "Native ETH restaking relies on beacon chain withdrawal credentials pointed to EigenPods"
  - id: lido
    type: staking_protocol
    scope: [ethereum]
    assets: [stETH, wstETH]
    note: "Largest single LST deposited into EigenLayer"
  - id: coinbase
    type: staking_protocol
    scope: [ethereum]
    assets: [cbETH]
  - id: rocket_pool
    type: staking_protocol
    scope: [ethereum]
    assets: [rETH]
  - id: avs_operators
    type: node_operator_set
    scope: [ethereum]
    note: "Operators register to run AVS tasks; slashing conditions defined per AVS"
  - id: eigenlayer_dao
    type: governance
    scope: [ethereum]
    note: "EigenLayer governance controls slashing veto, AVS registration, and upgrade authority"
active_risks:
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "AVS slashing conditions were live in production from 2024; slashing parameters for each AVS are novel and largely untested — a misconfigured or malicious AVS could slash large operator stakes, cascading to LST backing"
  - risk_id: operator_concentration
    deployment: ethereum
    note: "Top 10 EigenLayer operators hold approximately 70% of restaked stake; correlated failure or compromise of these operators would affect a majority of all AVS security guarantees simultaneously"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "EigenLayer governance (EigenFoundation multisig) controls the slashing veto mechanism — the entity with veto power can block or allow AVS slashing unilaterally, creating a single point of trust"
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "EigenLayer enforces a 7-day unbonding / unstaking delay for native ETH and LST restakers; during this window restakers cannot exit positions in response to AVS incidents or market stress"
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "EigenLayer core contracts are upgradeable proxies controlled by EigenFoundation multisig; a malicious or coerced upgrade could alter slashing conditions or drain operator stakes"
audits:
  - firm: Trail of Bits
    date: 2023-05
    url: ""
  - firm: Sigma Prime
    date: 2023-06
    url: ""
  - firm: OpenZeppelin
    date: 2023-07
    url: ""
  - firm: Certora
    date: 2023-08
    url: ""
---

## Overview

EigenLayer is the primary restaking protocol on Ethereum, allowing ETH stakers and
LST holders to extend cryptoeconomic security to Actively Validated Services (AVSs).
Stakers delegate stake to operators who opt into AVS tasks; in exchange for extra
yield they accept additional slashing conditions defined by each AVS. With $9.8B
in restaked assets, EigenLayer is the deepest shared-security marketplace in DeFi
and is itself a dependency of most major LRT protocols (ether.fi, Kelp, Renzo, etc.).

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Single chain (Ethereum mainnet) as of 2026-01. Cross-chain restaking is on roadmap
but not live; no deployment divergence applies.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Unstaking delay | 7 days (escrow period) |
| Slashing veto authority | EigenFoundation multisig |
| Max operator commission | Set per operator, no protocol cap |
| Native restaking method | EigenPod (withdrawal credentials redirect) |
| LST restaking method | Direct deposit into strategy contracts |
| Number of live AVSs | ~20 (as of early 2026) |
