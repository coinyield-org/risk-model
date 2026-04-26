---
slug: solv_btc
name: SolvBTC
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 490000000
    since: 2024-01-01
  - chain: bnb
    tvl_usd: 0
    since: 2024-02-01
    note: "SolvBTC minted on BNB Chain; backed by Ethereum-side BTC custody"
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-03-01
    note: "SolvBTC bridged to Arbitrum via Solv multi-chain infrastructure"
dependencies:
  - id: solv_protocol_team
    type: custodian
    scope: all_deployments
    note: "Solv Protocol team acts as BTC custodian; underlying BTC held off-chain or via BTC custodians"
  - id: btc_custodians
    type: custodian
    scope: all_deployments
    note: "Third-party BTC custodians may be used alongside Solv custody; specific custodian composition not fully disclosed"
  - id: babylon_protocol
    type: staking_protocol
    scope: [ethereum]
    note: "Solv integrates Babylon Protocol for BTC staking yield; Babylon AVS slashing conditions apply to staked BTC"
  - id: solv_multichain_bridge
    type: bridge
    scope: [bnb, arbitrum]
    note: "Solv-operated multi-chain bridge mints SolvBTC representations on BNB and Arbitrum"
active_risks:
  - risk_id: custodian_risk
    deployment: ethereum
    note: "Solv Protocol team controls BTC custody; there is no on-chain enforceability of BTC backing. Insolvency, regulatory action, or operational failure at the custodian layer would result in direct loss of the $490M BTC backing"
  - risk_id: minter_key_leak
    deployment: [ethereum, bnb, arbitrum]
    note: "Solv multi-chain contracts are controlled by team admin keys; compromise allows unauthorized minting of SolvBTC across all chains, diluting backing without corresponding BTC deposits"
  - risk_id: bridge_lock_backing_loss
    deployment: [bnb, arbitrum]
    note: "SolvBTC on BNB and Arbitrum is minted via Solv's cross-chain infrastructure; backing loss on the Ethereum custody side instantly renders all multi-chain SolvBTC unbacked with no per-chain buffer"
  - risk_id: per_deployment_divergence
    deployment: [bnb, arbitrum]
    note: "Each chain deployment has distinct smart contract risk and bridge trust assumptions. BNB chain's 21-validator consensus and Arbitrum's sequencer dependency create different failure modes per deployment that must be assessed independently"
audits: []
---

## Overview

SolvBTC is a wrapped BTC token issued by Solv Protocol, backed by BTC held in custody
by the Solv team and third-party custodians. It is deployed on Ethereum, BNB Chain,
Arbitrum, and Merlin (a BTC L2). Solv integrates Babylon Protocol to generate staking
yield on the underlying BTC, introducing restaking slashing surface on top of the
custodial risk. The fundamental risk is custodial: all BTC backing is concentrated
off-chain with no cryptographic proof of reserves enforced on-chain.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

BNB and Arbitrum deployments are minted via Solv's proprietary multi-chain bridge.
BNB chain deployment inherits BSC's 21-validator PoSA consensus risk. Arbitrum
deployment inherits Arbitrum sequencer dependency. All non-Ethereum deployments
are doubly exposed: Ethereum-side custody risk plus their native chain infrastructure
risk. Merlin (BTC L2) is not in scope for standard chain taxonomy.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| BTC custodian | Solv Protocol team + undisclosed third-party custodians |
| Babylon integration | BTC staking yield via Babylon Protocol |
| Proof of reserves | No verified on-chain PoR enforced |
| Multi-chain minting | Solv-operated bridge (BNB, Arbitrum, Merlin) |
| Contract upgradeability | Team admin keys |
