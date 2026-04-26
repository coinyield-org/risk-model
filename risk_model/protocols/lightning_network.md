---
slug: lightning_network
name: Lightning Network
types: []
deployments:
  - chain: bitcoin
    tvl_usd: 370000000
    since: 2018-03-15
    note: "TVL represents total channel capacity; funds are locked in on-chain multisig outputs, not a smart-contract protocol"
dependencies:
  - id: bitcoin_miners
    type: settlement_layer
    scope: [bitcoin]
    note: "On-chain Bitcoin miners confirm channel open/close transactions; miner censorship or reorganization can delay settlement"
  - id: ln_routing_nodes
    type: infrastructure
    scope: [bitcoin]
    note: "Large routing nodes (ACINQ, Bitfinex, Kraken, OKX) collectively control disproportionate channel capacity and routing paths"
  - id: bolt_protocol
    type: specification
    scope: [bitcoin]
    note: "BOLT (Basis of Lightning Technology) spec governs interoperability; divergent implementations may have consensus bugs"
active_risks:
  - risk_id: whale_concentration
    deployment: bitcoin
    note: "A small number of large routing nodes control the majority of channel capacity and payment routing paths; failure or deliberate closure by these nodes can fragment the network and degrade payment routing for dependent participants"
  - risk_id: bad_debt_socialization
    deployment: bitcoin
    note: "Channel routing fragility: channels must be funded on both sides to route payments; unbalanced channels require costly rebalancing or payments fail; systemic imbalance cannot be corrected on-chain without force-closing channels and incurring on-chain fees"
  - risk_id: single_keeper_dependency
    deployment: bitcoin
    note: "Watchtowers are required to detect and penalize fraudulent channel closures while a user is offline; if a user's watchtower is offline or compromised, a counterparty can broadcast an outdated state and steal channel funds without recourse"
  - risk_id: oracle_staleness
    deployment: bitcoin
    note: "Lightning Network channel capital is not visible on-chain until channels are closed; no oracle exists for real-time LN liquidity or routing capacity, making aggregated TVL figures inherently approximate and unverifiable"
audits: []
---

## Overview

Lightning Network is a Bitcoin Layer 2 payment channel network that enables fast,
low-cost BTC transactions by locking funds in 2-of-2 multisig outputs on-chain and
routing payments off-chain through a network of payment channels. It is not a smart
contract system — security relies on Bitcoin's scripting primitives (HTLC, CSV timelocks)
and the liveness of watchtower infrastructure to detect fraud. Channel capacity of ~$0.37B
represents locked on-chain BTC, not deposits in an upgradeable contract.

## Type-specific risks

Lightning Network has no formal DeFi type classification — it is a Bitcoin payment channel
protocol. The base risk profile differs fundamentally from EVM DeFi: there is no admin key,
no upgradeable contract, and no oracle in the traditional sense. Risks are operational and
network-topology in nature.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Settlement layer | Bitcoin mainnet |
| Channel model | 2-of-2 multisig HTLC |
| Fraud protection | Watchtowers (optional; user responsibility) |
| Total public channels (approx.) | ~50,000 |
| Total channel capacity (approx.) | ~5,000 BTC |
| Force-close delay | 144–2016 blocks (~1–14 days) |
| Smart contract surface | None (Bitcoin Script only) |
