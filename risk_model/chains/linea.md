---
id: linea
name: Linea
vm: evm_zkevm
consensus: zk_rollup
layer: L2
sequencer: consensys
sequencer_type: centralized_single
finality_to_l1: zk_proof_and_l1_settlement
l1: ethereum
native_bridge: linea_bridge
key_risks:
  - sequencer_operator_key_leak
  - sequencer_downtime
  - l2_finality_delay
  - l2_fee_spike_unprofitable
  - bridge_dep
  - mempool_censorship_infra
risk_notes:
  sequencer_downtime: >
    A centralized sequencer outage blocks new L2 transactions. Liquidations and
    oracle updates can be delayed while external markets continue moving.
  l2_finality_delay: >
    L2 soft confirmations are not the same as Ethereum settlement. Proof
    generation, posting, and L1 finality create delayed canonical finality.
  bridge_dep: >
    Canonical bridge operations and emergency controls are system-wide
    dependencies for assets moving between Ethereum and Linea.
  mempool_censorship_infra: >
    Sequencer-controlled ordering and inclusion create censorship and
    priority-flow risk for liquidation and arbitrage transactions.
defi_context:
  notes: >
    Linea is a Consensys zkEVM L2. DeFi deployments inherit Ethereum settlement
    security only after proof and L1 settlement; before that, they depend on
    centralized sequencing and bridge operation.
---

## Chain-specific risk profile

Linea is an Ethereum L2 with centralized sequencing and zk settlement to
Ethereum. Risk is split between fast local execution and delayed canonical
settlement.

## Sequencer assumptions

During sequencer downtime, users and liquidators cannot reliably submit or
settle new transactions on the L2, even if Ethereum and external markets are
healthy.

## Bridge assumptions

Linea bridge/admin controls can become a chain-wide dependency for bridged
collateral and cross-chain liquidity.

