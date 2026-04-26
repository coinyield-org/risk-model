---
id: bitcoin
name: Bitcoin
vm: bitcoin_script
consensus: proof_of_work
layer: L1
sequencer: null
finality_blocks: 6
finality_seconds: ~3600
l1: null
native_bridge: null
mev_infra: public_mempool
key_risks:
  - chain_reorg
  - rpc_infra_dep
  - bridge_dep
  - mempool_censorship_infra
risk_notes:
  chain_reorg: >
    Bitcoin finality is probabilistic. Short reorgs are normal, while deeper
    reorgs are economically expensive but still the relevant settlement risk
    for BTC-backed assets, staking derivatives, and bridge mint/burn flows.
  bridge_dep: >
    BTC used in DeFi is usually represented through custodial, federated, or
    bridge-issued wrappers. The chain itself does not provide native general
    purpose smart-contract bridging semantics.
  rpc_infra_dep: >
    Indexers and wallet/RPC providers are critical for detecting deposits,
    withdrawals, confirmations, and bridge mint/burn events.
  mempool_censorship_infra: >
    Transaction inclusion depends on miner policy and fee market conditions.
    During congestion, time-sensitive peg, bridge, and liquidation operations
    can become delayed or uneconomic.
defi_context:
  notes: >
    Bitcoin is mostly an upstream settlement and collateral layer in this risk
    model. DeFi exposure usually appears through wrapped BTC, BTC staking,
    Bitcoin L2s, or custodial BTC-backed tokens.
---

## Chain-specific risk profile

Bitcoin is not an application-chain environment like EVM or SVM chains. Its DeFi
risk mainly enters through wrappers, bridges, custodians, staking layers, and
indexers that interpret Bitcoin settlement.

## Finality model

Bitcoin has probabilistic PoW finality. Protocols should distinguish one-block
confirmation UX from economic finality assumptions used by bridges and
custodians.

## DeFi dependency pattern

The main cascade path is not "contract calls on Bitcoin". It is:

- BTC settlement / confirmations
- bridge or custodian interpretation
- wrapped BTC supply on another chain
- downstream lending, LP, or vault exposure

