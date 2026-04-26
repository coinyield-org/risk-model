---
id: tron
name: TRON
vm: tvm
consensus: delegated_proof_of_stake
layer: L1
sequencer: super_representatives
sequencer_type: delegated_validator_set
l1: null
native_bridge: null
key_risks:
  - chain_halt
  - chain_reorg
  - rpc_infra_dep
  - mempool_censorship_infra
  - governance_hostile_decision
  - operator_concentration
risk_notes:
  chain_halt: >
    TRON liveness depends on a delegated validator / super representative set.
    A coordinated outage or governance incident affects all TRON DeFi at once.
  chain_reorg: >
    Finality and rollback assumptions differ from Ethereum. Protocols should
    avoid importing Ethereum confirmation assumptions to TRON deployments.
  mempool_censorship_infra: >
    A smaller delegated block-producer set increases inclusion and censorship
    sensitivity for time-critical transactions.
  operator_concentration: >
    Concentration in super representatives makes validator/operator risk a
    chain-level assumption for TRON protocols.
  governance_hostile_decision: >
    Chain-level governance and ecosystem concentration can affect protocol
    operations, integrations, and asset flows.
defi_context:
  notes: >
    TRON has large stablecoin flow, especially USDT, and a separate DeFi
    ecosystem. Treat TRON deployments as their own settlement and governance
    domain.
---

## Chain-specific risk profile

TRON is a delegated validator L1 with a large stablecoin usage footprint. Its
risk profile is not Ethereum-like despite EVM-inspired tooling and DeFi
patterns.

## Stablecoin concentration

TRON DeFi often depends on USDT liquidity and issuer controls. Chain risk and
token issuer risk should be modeled separately but can compound during stress.

## Delegated validator assumptions

Super representative concentration creates liveness, inclusion, and governance
risks that matter for liquidations, bridge operations, and exits.

