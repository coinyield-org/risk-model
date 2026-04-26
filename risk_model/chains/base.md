---
id: base
name: Base
vm: evm_op_stack
consensus: optimistic_rollup
layer: L2
sequencer: coinbase
sequencer_type: centralized_corporate
finality_to_l1: 7_days_challenge_period
soft_finality: ~2s
l1: ethereum
native_bridge: base_bridge
fault_proof: cannon_single_round
key_risks:
  - sequencer_operator_key_leak
  - sequencer_downtime
  - l2_finality_delay
  - l2_fee_spike_unprofitable
  - issuer_corporate_risk
  - mempool_censorship_infra
risk_notes:
  sequencer_operator_key_leak: >
    Sequencer is operated by Coinbase — a public corporation, regulated by the SEC.
    This adds a unique vector: regulatory pressure can force
    Coinbase to censor tx or shut down the sequencer. Not hypothetically —
    Coinbase has already enforced OFAC compliance at the CEX level.
  issuer_corporate_risk: >
    USDC is the primary stablecoin on Base, Circle is Coinbase's partner. Double
    dependency: sequencer operator = USDC distribution partner. Their
    regulatory risk is mutually reinforcing.
  mempool_censorship_infra: >
    Coinbase as sequencer has monopoly control over tx ordering and
    inclusion. The MEV-boost analog on Base is less mature than on Ethereum.
notable_incidents:
  - date: 2023-08
    description: >
      Several short outages under high load after the launch of Base mainnet.
defi_context:
  growth_rate: high
  notes: >
    Fast-growing L2. Core ecosystem: Aerodrome, Morpho Base, Aave Base.
    Retail-oriented (Coinbase user funnel). Additional risk vs Arbitrum:
    corporate sequencer with compliance obligations.
---

## Chain-specific risk profile

Base is built on OP Stack (like Optimism). The main difference from other OP-chains is
the sequencer operated by Coinbase Inc., a publicly traded company in an SEC-regulated
jurisdiction.

## Corporate sequencer risk

The Coinbase sequencer creates a risk absent in Arbitrum (private company):
- SEC enforcement → forced shutdown or compliance mode
- Coinbase bankruptcy → sequencer unavailable
- Coinbase-USDC relationship → possible preferences in inclusion

This risk is still theoretical, but structurally built into the architecture.

## OP Stack shared codebase

Base and Optimism use a shared OP Stack codebase. Critical bug in OP Stack →
both chains are vulnerable simultaneously. This is a cross-chain infrastructure risk.

## Fault proofs

Base launched fault proofs in 2024. Before that the chain was in "training wheels" mode —
exclusively centralized. Current status: cannon single-round fault proofs,
decentralization roadmap in progress.
