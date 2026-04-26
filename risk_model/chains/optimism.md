---
id: optimism
name: OP Mainnet
vm: evm_op_stack
consensus: optimistic_rollup
layer: L2
sequencer: op_foundation
sequencer_type: centralized_nonprofit
finality_to_l1: 7_days_challenge_period
soft_finality: ~2s
l1: ethereum
native_bridge: optimism_bridge
fault_proof: cannon_single_round
key_risks:
  - sequencer_operator_key_leak
  - sequencer_downtime
  - l2_finality_delay
  - l2_fee_spike_unprofitable
  - mempool_censorship_infra
risk_notes:
  sequencer_operator_key_leak: >
    Sequencer is operated by the OP Foundation (nonprofit). Slightly less subject to
    regulatory pressure vs Coinbase, but still centralized.
  l2_fee_spike_unprofitable: >
    OP Mainnet was one of the first to switch to EIP-4844 blobs. Fee structure
    post-4844 has improved significantly, but blob market volatility remains.
notable_incidents:
  - date: 2021-11
    description: >
      Critical bug in OVM 1.0 Geth was discovered (not exploited).
      If an attacker had found it — they could have created infinite ETH on Optimism.
      Example: L2 codebase risk even without exploit.
defi_context:
  notes: >
    Large ecosystem: Synthetix, Velodrome, Aave V3 Optimism, Kwenta.
    Superchain vision: OP Stack as a standard for a family of L2s (Base, Zora,
    Mode, Redstone). Shared codebase risk is distributed across the entire Superchain.
---

## Chain-specific risk profile

OP Mainnet is the original Optimism, now part of the Superchain ecosystem.
OP Stack = shared codebase with Base, Zora and other OP chains.

## Superchain shared risk

A critical vulnerability in OP Stack affects all Superchain chains
simultaneously. This is a unique cross-chain infrastructure risk absent
in "standalone" L2s like Arbitrum.

## Governance token usage

OP token is used for governance of OP Foundation and Optimism Collective.
Governance decisions affect sequencer parameters, fee structure, chain
upgrades — all of this is downstream risk for DeFi protocols on the chain.
