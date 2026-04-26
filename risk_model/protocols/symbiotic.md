---
slug: symbiotic
name: Symbiotic
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 460000000
    since: 2024-06-01
dependencies:
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
    note: "Native ETH restaking routes through Ethereum beacon chain withdrawal credentials"
  - id: symbiotic_network_operators
    type: node_operator_set
    scope: [ethereum]
    note: "Operators in Symbiotic are analogous to AVS operators in EigenLayer; slashing conditions defined per network"
  - id: symbiotic_collateral_vaults
    type: collateral
    scope: [ethereum]
    note: "Collateral vaults hold staked assets (ETH, LSTs, ERC-20s); each vault has independent operator and network delegation"
  - id: symbiotic_governance
    type: governance
    scope: [ethereum]
    note: "Symbiotic governance controls slashing conditions, network registration, and upgrade authority over core contracts"
active_risks:
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "Symbiotic network slashing conditions are novel and largely untested — the protocol launched in 2024 with limited operational track record. A misconfigured or malicious network could trigger large-scale slashing of collateral vault assets, cascading to all depositors in affected vaults"
  - risk_id: operator_concentration
    deployment: ethereum
    note: "As a 2024-launch protocol, operator set is small and concentration risk is elevated. A small number of operators hold a disproportionate share of delegated stake; correlated failure or compromise would simultaneously impair security guarantees across multiple Symbiotic networks"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "Symbiotic governance controls slashing conditions and veto authority for network-triggered slashing events. A hostile or captured governance action could modify slashing parameters, whitelist malicious networks, or block legitimate slashing veto — all with direct impact on depositor principal"
  - risk_id: withdrawal_queue_delay
    deployment: ethereum
    note: "Symbiotic enforces operator unstaking delays (unbonding period per network); during this window depositors cannot exit in response to slashing incidents or adverse network behavior. Delay duration varies by network configuration and is not standardized"
  - risk_id: governance_signer_key_leak
    deployment: ethereum
    note: "Symbiotic core contracts were launched in 2024 with upgrade authority held by the Symbiotic team multisig; early-stage protocols often retain elevated admin key surface before transitioning to full governance control. Compromise enables arbitrary modification of vault accounting or slashing logic"
audits:
  - firm: Cyfrin
    date: 2024-06
    url: ""
  - firm: Statemind
    date: 2024-06
    url: ""
  - firm: Statemind
    date: 2024-07
    url: ""
  - firm: Statemind
    date: 2024-08
    url: ""
  - firm: Statemind
    date: 2024-09
    url: ""
  - firm: Statemind
    date: 2024-10
    url: ""
  - firm: Statemind
    date: 2024-11
    url: ""
  - firm: Statemind
    date: 2024-12
    url: ""
  - firm: Statemind
    date: 2025-01
    url: ""
---

## Overview

Symbiotic is a modular restaking protocol on Ethereum, launched in 2024 as an
alternative to EigenLayer. It allows stakers to deposit collateral (ETH, LSTs,
and arbitrary ERC-20 tokens) into permissioned vaults and delegate to network
operators who provide security to Symbiotic networks (analogous to EigenLayer AVSs).
Each vault, operator, and network is independently configured with its own slashing
conditions. With $460M TVL and a 2024 launch date, Symbiotic carries elevated
new-protocol risk on top of the structural restaking slashing surface.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Single chain (Ethereum mainnet) as of 2026-01. No cross-chain deployment divergence
applies. Future cross-chain expansion would introduce bridge and per-chain risks.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Protocol launch | June 2024 |
| Collateral types accepted | ETH, LSTs, arbitrary ERC-20 (vault-configurable) |
| Slashing authority | Per-network, governed by network operator + Symbiotic governance veto |
| Unbonding delay | Per-network configuration (no protocol-wide standard) |
| Upgrade authority | Symbiotic team multisig (early-stage) |
| Audit count | 9 audits (Cyfrin + Statemind) |
