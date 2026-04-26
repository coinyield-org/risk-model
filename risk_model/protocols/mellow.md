---
slug: mellow
name: Mellow Core (LRT infrastructure)
types: [lrt, yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 310000000
    since: 2024-02-01
dependencies:
  - id: symbiotic
    type: restaking_protocol
    scope: [ethereum]
    note: "Mellow's primary vault strategy routes capital through Symbiotic for restaking; Symbiotic slashing conditions directly affect Mellow vault NAV"
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    note: "Some Mellow vaults use EigenLayer as the restaking layer; EigenLayer slashing risk applies to these vaults"
  - id: lido
    type: staking_protocol
    scope: [ethereum]
    assets: [wstETH]
    note: "wstETH is the primary collateral asset in Mellow vaults; Lido withdrawal queue and stETH depeg risk affect vault liquidity"
  - id: mellow_governance
    type: governance
    scope: [ethereum]
    note: "Mellow governance (MELLOW token holders) controls vault strategy parameters, operator set selection, and protocol fee structure"
active_risks:
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "Mellow vaults are structurally dependent on Symbiotic and EigenLayer for restaking yield; a critical failure at either restaking layer — smart contract exploit, governance attack, or mass slashing event — directly and fully impacts all Mellow vault NAVs. There is no independent yield source to buffer restaking protocol failures"
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "Mellow's LRT vaults expose depositors to AVS (Actively Validated Service) slashing conditions on both Symbiotic and EigenLayer; AVS slashing is a new and partially untested risk vector — historical slashing data is limited, making quantitative risk assessment difficult"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "Mellow governance controls the allocation of vault capital across operators and restaking protocols; a hostile or miscalibrated governance decision — such as listing a high-risk AVS, changing rebalancing thresholds, or altering fee structures — could materially harm depositors without their consent"
  - risk_id: operator_concentration
    deployment: ethereum
    note: "Mellow vaults delegate restaking capital to a selected set of Symbiotic/EigenLayer operators; if a small number of operators receive the majority of delegated capital and those operators are slashed or go offline simultaneously, the impact on vault NAV is disproportionate relative to the number of operators in the set"
audits:
  - firm: Statemind
    date: 2024-03
    url: ""
  - firm: Ackee Blockchain
    date: 2024-04
    url: ""
  - firm: Oxorio
    date: 2024-05
    url: ""
  - firm: Statemind
    date: 2024-08
    url: ""
  - firm: Ackee Blockchain
    date: 2024-11
    url: ""
---

## Overview

Mellow Core is a modular LRT (Liquid Restaking Token) infrastructure protocol on Ethereum
that enables the creation of curated restaking vaults. Each Mellow vault routes depositor
capital (primarily wstETH) through Symbiotic or EigenLayer to generate restaking yield.
Mellow acts as the vault infrastructure and governance layer; operators and curators select
which AVSs and restaking protocols receive capital. The protocol has five audit reports
from reputable firms, making it better-audited than most comparably-sized LRT protocols.

## Type-specific risks

See `types/lrt.md` and `types/yield_aggregator.md` for base risk profiles.
