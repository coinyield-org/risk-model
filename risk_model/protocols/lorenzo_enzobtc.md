---
slug: lorenzo_enzobtc
name: Lorenzo enzoBTC
types: [bridge, lrt]
deployments:
  - chain: ethereum
    tvl_usd: 460000000
    since: 2024-06-01
    note: "enzoBTC minted on Ethereum; BTC backing held via Lorenzo Finance custodian"
  - chain: bnb
    tvl_usd: 0
    since: 2024-07-01
    note: "enzoBTC bridged to BNB Chain via Lorenzo multi-chain infrastructure"
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-08-01
    note: "enzoBTC bridged to Arbitrum"
dependencies:
  - id: lorenzo_finance_team
    type: custodian
    scope: all_deployments
    note: "Lorenzo Finance team holds BTC in custody; underlying BTC staked via Babylon Protocol"
  - id: babylon_protocol
    type: staking_protocol
    scope: all_deployments
    note: "Babylon provides the BTC staking layer; Lorenzo's yield is derived from Babylon AVS participation"
  - id: lorenzo_multichain_bridge
    type: bridge
    scope: [bnb, arbitrum]
    note: "Lorenzo-operated bridge mints enzoBTC on BNB and Arbitrum"
active_risks:
  - risk_id: custodian_risk
    deployment: ethereum
    note: "Lorenzo Finance team holds all underlying BTC; no on-chain enforceability of BTC backing. As a new protocol (2024 launch), the custodian track record is minimal — insolvency, operational failure, or regulatory action could result in total loss of the $460M BTC backing"
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "enzoBTC backing is staked via Babylon Protocol into AVSs; Babylon's slashing conditions are novel (2024 launch) with limited track record. A misconfigured or malicious AVS could slash the underlying BTC principal, directly reducing enzoBTC backing below 1:1"
  - risk_id: bridge_lock_backing_loss
    deployment: [bnb, arbitrum]
    note: "enzoBTC on BNB and Arbitrum is minted via Lorenzo's bridge; custody failure or backing loss on Ethereum instantly renders all multi-chain enzoBTC unbacked"
  - risk_id: minter_key_leak
    deployment: [ethereum, bnb, arbitrum]
    note: "Lorenzo is a new protocol (2024) with team-controlled admin keys; compromise allows unauthorized minting of enzoBTC across all chains, diluting BTC backing"
audits:
  - firm: Zellic
    date: 2024-07
    url: ""
---

## Overview

Lorenzo enzoBTC is a liquid BTC staking token issued by Lorenzo Finance. Users deposit
BTC, which Lorenzo custodies and stakes via Babylon Protocol into AVSs (Actively
Validated Services) to generate yield. enzoBTC is minted across Ethereum, BNB Chain,
and Arbitrum. As a 2024-launch protocol integrating two novel systems (BTC liquid
staking and Babylon AVS staking), enzoBTC carries compounded custodial and restaking
slashing risks with minimal operational track record.

## Type-specific risks

See `types/bridge.md` for custodial backing risk profile.
See `types/lrt.md` for AVS restaking risk profile.

## Deployment divergence

BNB and Arbitrum deployments are minted via Lorenzo's bridge and inherit both the
Ethereum-side custody risk and their respective chain infrastructure risks. BNB
deployment adds BSC's 21-validator PoSA risk; Arbitrum deployment adds sequencer
dependency. The Babylon integration creates a shared slashing surface across all
chain deployments simultaneously, as the underlying BTC stake is single and
undivided.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| BTC custodian | Lorenzo Finance team |
| Yield source | Babylon Protocol AVS staking |
| Protocol launch | 2024 (limited track record) |
| Audit coverage | 1 audit (Zellic, 2024) |
| Multi-chain | Ethereum, BNB, Arbitrum (Lorenzo bridge) |
| Babylon slashing | Active — novel conditions, limited precedent |
