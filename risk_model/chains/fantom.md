---
id: fantom
name: Fantom Opera
vm: evm
consensus: aBFT_pos
layer: L1
sequencer: null
l1: null
native_bridge: multichain_bridge
key_risks:
  - chain_reorg
  - rpc_infra_dep
  - bridge_dep
  - operator_concentration
  - mempool_censorship_infra
risk_notes:
  chain_reorg: >
    Fantom finality is fast under normal operation, but protocols should not
    assume Ethereum-like economic security or confirmation depth. Bridged and
    oracle-dependent protocols remain sensitive to rollback and settlement
    assumptions.
  rpc_infra_dep: >
    Smaller EVM ecosystems often depend on a thinner RPC/indexer set than
    Ethereum. Liquidators, bots, and monitoring pipelines can fail together.
  bridge_dep: >
    Fantom DeFi historically relied heavily on bridge-imported liquidity and
    wrapped assets. Bridge incidents propagate quickly into protocol solvency
    and exit liquidity.
  operator_concentration: >
    Validator and infrastructure concentration is more material than on larger
    L1s. A small set of operators can become a shared failure domain.
  mempool_censorship_infra: >
    Time-sensitive liquidations and arbitrage still depend on validator
    inclusion behavior and network-level transaction propagation.
defi_context:
  notes: >
    Fantom historically hosted bridge-heavy EVM DeFi. In this graph it appears
    mainly through incident evidence rather than current top-deployment count,
    but it should still be modeled as its own settlement domain.
---

## Chain-specific risk profile

Fantom is an EVM L1 with a smaller security, validator, and liquidity footprint
than Ethereum. Chain risk and bridge-backed asset risk often compound.

## Bridge-heavy ecosystem

A large share of historical Fantom DeFi exposure came from externally bridged
assets rather than native issuance. That makes bridge integrity central to chain
level risk.

## Operational concentration

Compared with larger L1s, validator, RPC, and indexer concentration matters
more for liquidation reliability and incident response.

