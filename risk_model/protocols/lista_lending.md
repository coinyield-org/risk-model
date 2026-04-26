---
slug: lista_lending
name: Lista Lending
primary: lista
types: [lending]
deployments:
  - chain: bnb
    tvl_usd: 570000000
    since: 2023-08-01
dependencies:
  - id: lista_dao
    type: governance
    scope: [bnb]
    note: "Lista DAO governs risk parameters, collateral listings, and contract upgrades"
  - id: lista_slisbnb
    type: collateral_protocol
    scope: [bnb]
    assets: [slisBNB]
    note: "slisBNB is the primary collateral; exchange rate from Lista LST feeds into liquidation logic"
  - id: chainlink
    type: oracle_provider
    scope: [bnb]
    note: "Chainlink BSC feeds provide price data; BSC deployment has fewer feeds and longer heartbeats than Ethereum mainnet"
active_risks:
  - risk_id: oracle_staleness
    deployment: bnb
    note: "Chainlink on BSC has fewer node operators and longer heartbeat intervals than Ethereum. During BSC network stress or chain halt, oracle feeds may not update, allowing stale prices to persist and creating bad debt risk on collateral positions"
  - risk_id: chain_halt
    deployment: bnb
    note: "BSC chain halts (as seen Oct 2022) freeze all lending operations — liquidations cannot execute during a halt, allowing undercollateralized positions to accumulate. This is a documented, non-hypothetical risk on BSC"
  - risk_id: governance_hostile_decision
    deployment: bnb
    note: "Lista DAO controls LTV ratios, liquidation bonuses, and debt ceilings for all collateral types including slisBNB; a hostile governance action could set parameters enabling systemic bad debt"
audits: []
---

## Overview

Lista Lending is the lending arm of the Lista ecosystem on BNB Smart Chain, using
slisBNB and other BSC assets as collateral. It is operationally and governance-linked
to Lista Liquid Staking; no independent audit PDFs have been indexed — see `lista.md`
for audit coverage of shared Lista DAO contracts.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Inherits all BSC infrastructure risks documented in `lista.md`: 21-validator
consensus, chain halt precedent, and thinner Chainlink oracle coverage relative
to Ethereum deployments. slisBNB collateral adds LST exchange-rate risk on top
of standard lending collateral risk.
