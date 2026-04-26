---
id: polygon
name: Polygon PoS
vm: evm
consensus: pos_bor_heimdall
layer: sidechain
sequencer: null
validator_count: ~100
validator_stake_token: POL
finality_seconds: ~2-3
l1: ethereum
native_bridge: polygon_pos_bridge
trust_model: federated_checkpoints
key_risks:
  - chain_reorg
  - rpc_infra_dep
  - governance_signer_key_leak
  - bridge_dep
  - validator_avs_slashing
risk_notes:
  trust_model: >
    Polygon PoS is not a trustless rollup. It is a federated PoS chain with checkpoints
    on Ethereum every ~30 min. Security is determined by ~100 validators,
    not Ethereum L1 security. For withdrawing funds to Ethereum — checkpoint
    finality is required, but a bridge compromise is possible via validator collusion.
  bridge_dep: >
    Polygon PoS Bridge uses a multisig for emergency actions. In 2021
    a vulnerability was uncovered: the Plasma exit game was insecure. Bridge trust
    assumptions are weaker than those of optimistic/ZK rollups.
  chain_reorg: >
    100 validators — enough for an attack under stake concentration. Historically
    short reorgs have been observed. Finality is faster than Ethereum, but less
    guaranteed.
notable_incidents:
  - date: 2021-12
    description: >
      Critical bug in the Polygon PoS contract — 9.27B MATIC potentially
      vulnerable. Fixed with a silent hardfork without public announcement.
      Example: sidechain can do silent upgrades.
  - date: 2022-03
    description: >
      Polygon officially confirmed a $2M exploit via a vulnerability in the Bridge
      (a separate incident from Plasma).
defi_context:
  notes: >
    Aave V3 Polygon, Quickswap, Balancer. TVL is declining relative to L2s.
    Polygon AggLayer (ZK-based) is the next generation, a different risk profile.
    The current PoS chain remains primary for legacy protocols.
---

## Chain-specific risk profile

Polygon PoS is not a rollup, but a standalone PoS sidechain with checkpoints on
Ethereum. The key difference from L2: security budget does not inherit from Ethereum.

## Bridge trust model

Canonical Polygon bridge requires trust in ~100 validators + multisig emergency
admin. This is substantially weaker than the cryptographic security of a ZK-rollup or
the economic security of an optimistic-rollup with honest watchers.

## Silent upgrade precedent

In 2021 Polygon performed an emergency hardfork without public announcement,
fixing a critical bug. Technically this demonstrates the possibility of a sudden
protocol change without governance process. Precedent relevant for trust model.
