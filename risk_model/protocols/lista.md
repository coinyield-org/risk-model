---
slug: lista
name: Lista Liquid Staking (slisBNB)
types: [lst]
deployments:
  - chain: bnb
    tvl_usd: 610000000
    since: 2023-05-01
dependencies:
  - id: bnb_chain_validators
    type: validator_set
    scope: [bnb]
    note: "BNB Smart Chain operates with only 21 active validators; Lista delegates staked BNB across this set"
  - id: lista_dao
    type: governance
    scope: [bnb]
    note: "Lista DAO (LISTA token holders) controls protocol parameters, fee structure, and upgrade authority"
  - id: slisbnb_oracle
    type: oracle_provider
    scope: [bnb]
    note: "slisBNB exchange rate oracle consumed by Lista Lending and third-party integrations"
active_risks:
  - risk_id: operator_concentration
    deployment: bnb
    note: "BNB Smart Chain has only 21 active validators; the entire slisBNB backing is distributed across this highly concentrated set. Correlated failure, collusion, or regulatory action against a supermajority of BSC validators would impair slisBNB redemption"
  - risk_id: chain_halt
    deployment: bnb
    note: "BSC has a documented history of chain halts (Oct 2022: $100M exploit triggered manual halt by validator coordination). A chain halt freezes all slisBNB operations including minting, redemption, and liquidations in downstream protocols"
  - risk_id: exchange_rate_vs_market_depeg
    deployment: bnb
    note: "slisBNB accrues BNB staking rewards via exchange rate; secondary market liquidity on BSC DEXs is thin relative to staked TVL. During BNB market stress or Lista-specific events, slisBNB can trade at material discount before redemption arbitrage restores peg"
  - risk_id: governance_hostile_decision
    deployment: bnb
    note: "Lista DAO governance controls operator selection, fee parameters, and smart contract upgrades; a hostile or low-turnout DAO vote could alter withdrawal mechanics or redirect protocol fees"
  - risk_id: governance_signer_key_leak
    deployment: bnb
    note: "Lista protocol contracts are upgradeable; compromise of the admin multisig allows arbitrary modification of staking logic, fee parameters, or withdrawal credentials"
audits:
  - firm: PeckShield
    date: 2023-06
    url: ""
  - firm: PeckShield
    date: 2023-09
    url: ""
  - firm: PeckShield
    date: 2024-01
    url: ""
  - firm: SlowMist
    date: 2023-07
    url: ""
  - firm: SlowMist
    date: 2023-11
    url: ""
  - firm: SlowMist
    date: 2024-02
    url: ""
---

## Overview

Lista Liquid Staking issues slisBNB, a liquid staking token representing staked BNB
on BNB Smart Chain. Users deposit BNB and receive slisBNB, which accrues validator
rewards via an appreciating exchange rate. The protocol is governed by Lista DAO and
operates within the constraints of BSC's 21-validator PoSA consensus model. slisBNB
is the primary collateral asset in Lista Lending and several BSC DeFi integrations.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

Single chain (BNB Smart Chain) deployment. BSC's concentrated validator set (21
validators vs Ethereum's ~1M) and historical chain halt precedent introduce
infrastructure risks not present in Ethereum-based LSTs. Withdrawal finality
depends on BSC consensus liveness rather than Ethereum beacon chain exit queues.

## Key parameters (bnb, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Validators (active) | 21 (BSC PoSA) |
| Staking reward source | BNB validator block rewards + MEV |
| Protocol fee | Portion of staking rewards → Lista DAO treasury |
| Redemption mechanism | Unstaking via BSC unbonding period |
| Governance token | LISTA |
| Contract upgradeability | Admin multisig (Lista DAO) |
