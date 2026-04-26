---
slug: arbitrum_bridge
name: Arbitrum Bridge (Nitro)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 1400000000
    since: 2021-08-31
  - chain: arbitrum
    tvl_usd: 0
    since: 2021-08-31
dependencies:
  - id: arbitrum_sequencer
    type: sequencer
    scope: [arbitrum]
  - id: offchain_labs
    type: governance_actor
    scope: [arbitrum]
  - id: arbitrum_dao
    type: governance_token
    scope: [arbitrum]
  - id: bold_challenge_protocol
    type: fraud_proof_system
    scope: [arbitrum]
active_risks:
  - risk_id: sequencer_downtime
    deployment: arbitrum
    severity_override:
      likelihood: 4
      note: "Offchain Labs single sequencer: documented Dec 2023 outage ~1.5h, Jan 2022 outage ~45min — users cannot exit via fast path during downtime"
  - risk_id: timelock_skew_cross_chain
    deployment: [ethereum, arbitrum]
    note: "7-day fraud proof challenge window for withdrawals from Arbitrum to Ethereum; assets locked for full window before L1 finality"
  - risk_id: proxy_upgrade_authority
    deployment: [ethereum, arbitrum]
    note: "Arbitrum Security Council (9/12 multisig) can execute emergency upgrades to bridge contracts without standard governance delay"
  - risk_id: governance_hostile_decision
    deployment: arbitrum
    note: "ARB governance (Arbitrum DAO) controls non-emergency upgrades and parameter changes; large ARB holders can direct protocol changes"
audits:
  - firm: Trail of Bits
    date: 2023-06
    url: ""
  - firm: Trail of Bits
    date: 2023-09
    url: ""
  - firm: Trail of Bits
    date: 2024-01
    url: ""
  - firm: Trail of Bits
    date: 2024-06
    url: ""
---

## Overview

The Arbitrum Bridge (Nitro) is the canonical L1↔L2 bridge connecting Ethereum
mainnet to Arbitrum One. Users deposit ETH and ERC-20 tokens on Ethereum, which
are locked in the bridge contract, with equivalent tokens issued on Arbitrum.
Withdrawals from Arbitrum to Ethereum are subject to a 7-day fraud proof
challenge window (BOLD protocol). The bridge holds approximately $1.4B in locked
assets. Offchain Labs operates the single sequencer; the Arbitrum Security
Council (9/12 multisig) can execute emergency upgrades.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

The bridge spans two chains (Ethereum L1 and Arbitrum L2) with asymmetric
finality guarantees:
- Ethereum → Arbitrum (deposits): fast (~10 min); no challenge period
- Arbitrum → Ethereum (withdrawals): 7-day challenge window before L1 finality
- During sequencer downtime, users can submit transactions via the delayed inbox
  (force-include after 24h), but this path is not well-known to end users

## Key parameters (as of 2026-01)

| Parameter | Value | Risk note |
|-----------|-------|-----------|
| Challenge period | 7 days | Long finality window for L1 withdrawals |
| Security Council | 9/12 multisig | Emergency upgrade authority; bypasses governance |
| Sequencer | Single (Offchain Labs) | Documented outages: Dec 2023 ~1.5h, Jan 2022 ~45min |
| Force-include delay | 24 hours | Fallback for sequencer censorship/downtime |
| ARB governance timelock | Variable (proposal-dependent) | Non-emergency changes subject to full DAO process |
