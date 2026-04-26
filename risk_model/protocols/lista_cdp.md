---
slug: lista_cdp
name: Lista CDP
types: [cdp]
deployments:
  - chain: bnb
    tvl_usd: 400000000
    since: 2023-06-01
dependencies:
  - id: lista_dao
    type: governance
    scope: all_deployments
  - id: lista
    type: staking_protocol
    scope: all_deployments
    assets: [slisBNB]
    note: primary collateral source (see 62_lista)
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: BNB/USD and slisBNB feeds on BSC
active_risks:
  - risk_id: oracle_staleness
    deployment: bnb
    note: "BSC Chainlink feeds have historically longer heartbeats and fewer fallback mechanisms than Ethereum mainnet feeds"
  - risk_id: ltv_too_aggressive
    note: "slisBNB collateral carries staking-redemption risk on top of BNB price volatility; rapid BNB moves can breach LTV before liquidation"
  - risk_id: governance_hostile_decision
    note: "Lista DAO controls collateral types, risk parameters, and fee structure; token concentration can enable parameter changes harmful to borrowers"
  - risk_id: chain_halt
    note: "BSC validator set (21 validators) is materially more centralized than Ethereum; chain halt or reorg affects all positions and oracle updates"
audits: []
---

## Overview

Lista CDP is the stablecoin minting module of the Lista protocol on BNB Chain.
Users collateralize slisBNB (Lista's liquid staking BNB) to mint lisUSD. The
protocol is closely integrated with the Lista liquid staking product (see `62_lista`)
and shares its governance and oracle dependencies. Audit coverage is addressed under
the Lista parent protocol; no separate CDP-specific PDFs are indexed.

## Type-specific risks

See `types/cdp.md` for base risk profile.
