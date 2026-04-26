---
id: arbitrum
name: Arbitrum One
vm: evm_nitro
consensus: optimistic_rollup
layer: L2
sequencer: offchain_labs
sequencer_type: centralized_single
finality_to_l1: 7_days_challenge_period
soft_finality: ~250ms
l1: ethereum
native_bridge: arbitrum_bridge
fault_proof: multi_round_interactive
key_risks:
  - sequencer_operator_key_leak
  - sequencer_downtime
  - l2_finality_delay
  - l2_fee_spike_unprofitable
  - mempool_censorship_infra
  - chain_reorg
risk_notes:
  sequencer_downtime: >
    Observed: December 2023 (~1.5 hours), January 2022 (~45 min).
    During downtime: transactions are not included, liquidations are impossible,
    prices continue to move on other markets.
  l2_finality_delay: >
    7-day challenge period before finality on L1. This means that
    withdrawals to Ethereum take 7 days through the canonical bridge.
    For DeFi protocols this is not critical, but for cross-chain messaging it creates
    asymmetry: deposit is fast, withdraw is slow.
  sequencer_operator_key_leak: >
    Single sequencer controlled by Offchain Labs. Compromise → inclusion
    censorship or reordering. Governance upgrade path exists, but is slow.
  l2_fee_spike_unprofitable: >
    Arbitrum fee = L2 execution + L1 data posting cost. During L1 congestion
    (blob fee spikes, post EIP-4844 base cost) L2 tx get more expensive.
    Liquidation bots may find it unprofitable to liquidate small positions.
notable_incidents:
  - date: 2023-12-15
    description: >
      Sequencer downtime ~1.5 hours due to a bug in sequencer software.
      Transactions accumulated in the mempool, none were executed.
  - date: 2022-01-09
    description: >
      Sequencer offline ~45 minutes. First public major outage.
defi_context:
  tvl_rank: 2
  notes: >
    Largest L2 by TVL. Aave V3, GMX, Pendle, Camelot — all deployed.
    DeFi on Arbitrum de facto accepts centralized sequencer risk as baseline.
    Sequencer failure → temporary freeze of all DeFi on the chain.
---

## Chain-specific risk profile

Arbitrum is an EVM-equivalent optimistic rollup. The main characteristic is
a single centralized sequencer (Offchain Labs). This is simultaneously a performance
advantage (~250ms soft finality) and a structural risk.

## Sequencer trust assumptions

Sequencer can:
- Censor tx (not include them)
- Reorder tx (front-run, though protected by mechanisms)
- Be offline (has happened historically)

Sequencer CANNOT (with fraud proofs):
- Publish invalid state transitions on L1
- Steal funds without detection

## Oracle considerations

On Arbitrum the Chainlink Sequencer Uptime Feed check is mandatory. Without it:
stale prices after sequencer downtime are served as fresh.
Aave V3 on Arbitrum has this check. Younger protocols often do not.

## Blob cost dependency

Post EIP-4844: Arbitrum uses blob transactions for data posting.
During blob fee spikes (possible under high L1 usage) the cost of L2 tx rises.
