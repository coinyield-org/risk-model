---
slug: hyperliquid
name: Hyperliquid Bridge
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 4700000000
    since: 2023-10-01
    note: "Ethereum-side bridge lock; funds transit to Hyperliquid L1"
dependencies:
  - id: hyperliquid_validators
    type: validator_set
    scope: all_deployments
    note: "~20 permissioned validators running HyperBFT consensus; set controlled by Hyperliquid foundation"
  - id: hyperliquid_foundation
    type: governance
    scope: all_deployments
    note: "Controls validator admission, protocol upgrades, and bridge parameters"
  - id: hype_token
    type: governance_token
    scope: all_deployments
    note: "HYPE token used for governance; Hyper Labs holds significant allocation"
active_risks:
  - risk_id: guardian_key_leak
    deployment: ethereum
    note: "~20 permissioned validators; compromise of a small subset can reach BFT threshold for unauthorized bridge withdrawals — materially lower attack cost than Ethereum mainnet validator set"
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "HYPE governance and Hyperliquid foundation control bridge upgrade paths and validator set composition; concentrated token allocation at Hyper Labs creates unilateral control risk"
  - risk_id: bridged_backing_loss
    deployment: ethereum
    note: "All $4.7B of user USDC is locked in the Ethereum bridge contract; any bridge exploit or validator collusion to forge withdrawal proofs results in total loss of locked funds"
  - risk_id: whale_coordination
    deployment: ethereum
    note: "Hyper Labs' large HYPE allocation means a small number of insiders can coordinate governance votes that affect bridge security parameters without broad community consent"
  - risk_id: sequencer_downtime
    deployment: ethereum
    note: "Hyperliquid L1 uses a centralized order-matching engine (HyperBFT); extended sequencer downtime freezes all bridge operations and strands deposited funds"
audits:
  - firm: Cyfrin
    date: 2024-06
    url: ""
---

## Overview

Hyperliquid operates a proprietary Layer-1 blockchain (HyperBFT consensus) optimized for
on-chain perpetuals trading. The bridge locks USDC and other assets on Ethereum and mirrors
balances on Hyperliquid L1. The validator set is small (~20 permissioned nodes) and is
controlled by the Hyperliquid foundation, making the bridge security model materially more
centralized than Ethereum-native solutions. In this model the bridge / entry layer lives
in `hyperliquid.md`, while the perp counterparty vault is modeled separately in
`hyperliquid_hlp.md`.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Bridge TVL (Ethereum) | ~$4.7B |
| Validator set size | ~20 permissioned validators |
| Consensus | HyperBFT (BFT variant) |
| BFT threshold | 2/3 of validator stake |
| Bridge upgrade authority | Hyperliquid foundation multisig |
