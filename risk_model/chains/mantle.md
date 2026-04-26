---
id: mantle
name: Mantle
vm: evm
consensus: optimistic_rollup
layer: L2
sequencer: mantle_network
sequencer_type: centralized_single
finality_to_l1: challenge_period
l1: ethereum
native_bridge: mantle_bridge
key_risks:
  - sequencer_operator_key_leak
  - sequencer_downtime
  - l2_finality_delay
  - l2_fee_spike_unprofitable
  - bridge_dep
  - rpc_infra_dep
risk_notes:
  sequencer_downtime: >
    Centralized sequencing means a Mantle outage pauses transaction inclusion
    for all DeFi deployments on the chain.
  l2_finality_delay: >
    Local L2 confirmation and Ethereum-finalized withdrawal are different
    states. Cross-chain users face delayed canonical finality.
  bridge_dep: >
    Mantle assets and external liquidity rely on bridge paths to Ethereum and
    other venues. Bridge pause or message delay directly affects exit liquidity.
  rpc_infra_dep: >
    Liquidators and keeper networks on smaller L2s can be sensitive to limited
    RPC/provider redundancy.
defi_context:
  notes: >
    Mantle is an Ethereum L2 with EVM-compatible DeFi. Risk is closer to other
    centralized-sequencer L2s than to Ethereum mainnet.
---

## Chain-specific risk profile

Mantle should be modeled as an L2 settlement domain with centralized sequencing,
bridge dependency, and delayed L1 finality.

## Liquidation and exit risk

During sequencer or RPC degradation, liquidation bots can miss time-sensitive
positions. Bridge delays then affect users trying to exit stressed assets.

## Data and bridge dependency

Mantle deployments can share dependencies with Ethereum protocols but still
need their own chain-level liveness and bridge-risk assumptions.

