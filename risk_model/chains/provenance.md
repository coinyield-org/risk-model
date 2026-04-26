---
id: provenance
name: Provenance Blockchain
vm: cosmos_sdk
consensus: tendermint_bft
layer: appchain
sequencer: null
l1: null
native_bridge: ibc
key_risks:
  - chain_halt
  - chain_reorg
  - rpc_infra_dep
  - bridge_dep
  - governance_hostile_decision
risk_notes:
  chain_halt: >
    Cosmos SDK/Tendermint-style appchains can halt if validator consensus or
    application logic cannot progress.
  chain_reorg: >
    Tendermint finality is fast under normal operation, but network partitions
    or validator-set faults still matter for availability and recovery.
  bridge_dep: >
    External DeFi consumption of Provenance assets depends on IBC, bridges, or
    custodial/tokenization routes.
  governance_hostile_decision: >
    Appchain governance can directly affect parameters, asset administration,
    validators, and integrations.
defi_context:
  notes: >
    Provenance is used for financial/RWA-style issuance. Risk model should
    separate chain liveness from issuer, legal, and custody risk.
---

## Chain-specific risk profile

Provenance is an appchain environment. For the current graph, it mainly appears
as the settlement chain for RWA/financial-market protocols.

## Appchain governance

Governance and validator-set decisions can have direct effects on chain
availability and asset operations.

## Bridge and integration path

When assets leave the native appchain environment, bridge and custody paths
become the main cross-chain risk vector.

