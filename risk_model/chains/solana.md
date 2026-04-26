---
id: solana
name: Solana
vm: svm
consensus: poh_tower_bft
layer: L1
sequencer: null
validator_count: ~1500_active
validator_stake_token: SOL
finality_seconds: ~0.4
l1: null
native_bridge: wormhole
mev_infra: jito
key_risks:
  - chain_halt
  - rpc_infra_dep
  - bridge_dep
  - sequencer_downtime
  - governance_signer_key_leak
risk_notes:
  chain_halt: >
    Solana has the largest number of production outages among major L1s:
    2021-09 (17h), 2021-12, 2022-01, 2022-04, 2022-06, 2023-02.
    Causes vary: transaction storm, bug in consensus, network partition.
    Unlike sequencer downtime (only one L2), a Solana halt affects
    all Solana DeFi protocols simultaneously.
  vm_difference: >
    SVM (Solana VM) is not EVM. Account model instead of contract model. Parallel
    transaction execution requires explicit account locks. Different
    composability model — not "any contract can call any contract" as in EVM.
  bridge_dep: >
    Wormhole is the native Solana bridge. Hacked in February 2022 ($320M).
    Most wrapped assets on Solana go through Wormhole.
  jito_mev: >
    Jito is MEV infrastructure on Solana. Jito-Solana validators have
    MEV bundling via block engine. Block building concentration at Jito.
notable_incidents:
  - date: 2021-09-14
    description: >
      17-hour network outage. Cause: transaction flood from an IDO. Consensus
      was overloaded, memory overflow. First major outage.
  - date: 2022-02-02
    description: >
      Wormhole bridge exploit: $320M. Attack on a signature verification bug
      on the Solana side. Largest bridge exploit at the time.
  - date: 2022-06
    description: >
      4.5-hour outage caused by a bug in durable nonce processing. Chain restart.
  - date: 2023-02-25
    description: >
      20-hour degraded performance due to a bug in QUIC implementation.
defi_context:
  notes: >
    Jupiter, Marinade Finance, Kamino, Orca, Raydium, MarginFi.
    Solana DeFi has a different composability model. Synchronous calls between
    protocols are limited by account locking. Atomic composability is a different
    risk model than in EVM.
---

## Chain-specific risk profile

Solana is a non-EVM L1 with a fundamentally different risk profile. Frequent outages,
a different composability model, Wormhole as dominant bridge.

## Non-EVM composability

In EVM any contract can call any other in one tx (Aave flash loan →
Uniswap → Aave). On Solana: all accounts that a tx will read/write
must be declared upfront. This limits the complexity of composability
but also changes the attack vector model.

## Outage risk model

Solana outages happen for various reasons (network storm, consensus bug,
implementation bug). The probability of an outage in an arbitrary 30-day period
has historically been non-zero. DeFi protocols on Solana should have a separate
uptime risk assessment.

## Jito block engine

The Jito-Solana client has >50% validator adoption. Jito block engine has
monopoly access to MEV bundling. This creates centralization similar to
Flashbots on Ethereum, but with less mature competitive ecosystem.
