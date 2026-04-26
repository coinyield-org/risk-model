---
slug: merlins_seal
name: Merlin's Seal
types: [bridge]
deployments:
  - chain: merlin_chain
    tvl_usd: 460000000
    since: 2024-01-01
dependencies:
  - id: merlin_chain
    type: underlying_chain
    scope: all_deployments
  - id: merlin_team
    type: operator
    scope: all_deployments
    note: sequencer + validator set
  - id: btc_custodians
    type: custodian
    scope: all_deployments
    assets: [BTC]
active_risks:
  - risk_id: guardian_key_leak
    note: "BTC held in multi-sig controlled by Merlin team — custodian key compromise = irreversible BTC loss"
  - risk_id: sequencer_downtime
    note: "Merlin Chain single sequencer operated by Merlin team; no decentralized fallback"
  - risk_id: bridged_backing_loss
    note: "BTC locked on L1 and bridged to merlin_chain — bridge integrity is sole backing guarantee"
  - risk_id: deployer_key_leak
    note: "Merlin team controls upgrade keys; no timelock observed on new BTC L2"
  - risk_id: chain_halt
    note: "Merlin Chain is a new BTC L2; consensus failure or sequencer crash halts all activity"
audits: []
---

## Overview

Merlin's Seal is the canonical bridge for Bitcoin to Merlin Chain, a BTC-native L2.
Users lock BTC on the Bitcoin L1; Merlin's Seal mints a wrapped representation on
Merlin Chain. The entire TVL (~$0.46B) is backed by BTC held in multi-sig custody
controlled by the Merlin team. As a newly launched BTC L2, the sequencer and
validator infrastructure remains highly centralized.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Single deployment on Merlin Chain; no multi-chain divergence.
Merlin Chain itself is a new ecosystem — finality guarantees, sequencer uptime SLAs,
and validator decentralization are materially weaker than established EVM L2s.
