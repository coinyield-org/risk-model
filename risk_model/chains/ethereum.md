---
id: ethereum
name: Ethereum Mainnet
vm: evm
consensus: pos_gasper
layer: L1
sequencer: null
finality_slots: 64
finality_seconds: ~780
tps_sustained: ~15
l1: null
native_bridge: null
mev_infra: flashbots_mev_boost
key_risks:
  - chain_reorg
  - builder_relay_dep
  - rpc_infra_dep
  - mempool_censorship_infra
risk_notes:
  chain_reorg: >
    Before finality (~13 min) reorg is possible. After the Merge the probability has decreased,
    but is not zero: attester slashing + proposer boost = finality-violating reorg
    is theoretically possible with >33% stake.
  builder_relay_dep: >
    >90% of blocks go through MEV-boost. Builder concentration: top-3 builders
    produce ~70% of blocks. Censorship at the builder level has actually been observed
    (OFAC-compliance in 2022-2023).
  rpc_infra_dep: >
    Infura/Alchemy serve the majority of public RPC endpoints.
    Their downtime = blindness of liquidation bots and frontends.
  mempool_censorship_infra: >
    Private order flow (Flashbots Protect) has captured ~30% of tx. Part of
    liquidations go through private relay — this is both protection and risk:
    dependency on relay operator.
notable_incidents:
  - date: 2022-08
    description: >
      OFAC-compliant builders began censoring Tornado Cash addresses.
      Censorship peak: ~72% of blocks from OFAC-compliant builders. Precedent of
      protocol-level censorship on production L1.
defi_context:
  largest_tvl_share: true
  notes: >
    Ethereum is the settlement layer for most L2s. Finality on Ethereum =
    final security for Optimistic/ZK rollups.
    Most bridges use Ethereum as an anchor of trust.
---

## Chain-specific risk profile

Ethereum is the most resilient and decentralized of the EVM chains. Risks here
are more subtle than on L2: no single sequencer, but there is builder centralization and
MEV infra concentration.

## Gas economics and liquidation risk

High gas cost on Ethereum means that under congestion small positions
(< $5-10K) become economically unprofitable to liquidate. Protocols must
take this into account when setting supply/borrow cap for low-liquidity assets.

## MEV ecosystem

Ethereum has the most mature MEV market. This is a double-edged risk:
- Competitive liquidation bots → positions are closed quickly
- Builder centralization → censorship vector
- Private mempool → invisibility of part of the flow for on-chain monitoring

## Finality model

Soft finality: 1 slot (~12 sec). Finality: 2 epochs (~12.8 min). Protocols
that accept deposits based on 1-2 block confirmations are exposed to reorg-risk.
