---
slug: usdt0
name: USDT0 / LayerZero OFT
types: [messaging]
deployments:
  - chain: ethereum
    tvl_usd: 3800000000
    since: 2024-01-01
    note: "Canonical USDT source; OFT adapter locks USDT and mints USDT0 on destination chains"
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-01-01
    note: "OFT deployment; USDT0 minted by LayerZero message from Ethereum"
  - chain: optimism
    tvl_usd: 0
    since: 2024-01-01
    note: "OFT deployment"
  - chain: bnb
    tvl_usd: 0
    since: 2024-01-01
    note: "OFT deployment"
  - chain: avalanche
    tvl_usd: 0
    since: 2024-01-01
    note: "OFT deployment"
dependencies:
  - id: layerzero_endpoint
    type: bridge
    scope: all_deployments
    note: "LayerZero V2 endpoint contracts on each chain; message passing layer"
  - id: layerzero_dvn
    type: bridge
    scope: all_deployments
    note: "Default DVN (LayerZero Labs) + Nethermind DVN required to attest cross-chain messages"
  - id: tether
    type: issuer
    scope: [ethereum]
    assets: [USDT]
    note: "Tether issues and can freeze/blacklist canonical USDT on Ethereum"
  - id: stargate_v2
    type: liquidity
    scope: all_deployments
    note: "Provides liquidity routing for USDT0 cross-chain transfers"
active_risks:
  - risk_id: guardian_key_leak
    deployment: all_deployments
    note: "Compromise of the LayerZero DVN set (LayerZero Labs + Nethermind) allows forging arbitrary cross-chain messages, enabling uncollateralized USDT0 minting on destination chains"
  - risk_id: per_deployment_divergence
    deployment: [arbitrum, optimism, bnb, avalanche]
    note: "Each OFT deployment has independently configured DVN thresholds, executor settings, and security parameters; misconfiguration on one chain does not affect others but creates a fragmented risk surface requiring per-chain monitoring"
  - risk_id: bridged_backing_loss
    deployment: [arbitrum, optimism, bnb, avalanche]
    note: "Non-Ethereum USDT0 supply is backed only by the OFT lock on Ethereum; any failure in the LayerZero message path or Ethereum-side contract creates a supply/backing mismatch"
  - risk_id: proxy_upgrade_authority
    deployment: all_deployments
    note: "LayerZero endpoint contracts are upgradeable; the upgrade authority (LayerZero Labs) can modify message verification logic affecting all OFT tokens that rely on the endpoint"
  - risk_id: message_replay_ordering
    deployment: all_deployments
    note: "Cross-chain OFT transfers depend on correct nonce ordering; message replay or out-of-order delivery can cause double-credit or stuck transfers without explicit on-chain replay protection per chain"
audits:
  - firm: LayerZero Labs / external (DVN audit)
    date: 2023-09
    url: ""
  - firm: LayerZero Labs / external (OFT audit 1)
    date: 2023-11
    url: ""
  - firm: LayerZero Labs / external (OFT audit 2)
    date: 2024-01
    url: ""
  - firm: LayerZero Labs / external (OFT audit 3)
    date: 2024-03
    url: ""
---

## Overview

USDT0 is a LayerZero OFT (Omnichain Fungible Token) wrapper around Tether's USDT.
Canonical USDT on Ethereum is locked in an OFT adapter; USDT0 is minted on destination
chains (Arbitrum, Optimism, BNB Chain, Avalanche) via LayerZero V2 cross-chain messages.
Security of the cross-chain supply relies on the DVN set (LayerZero Labs + Nethermind)
independently verifying messages on each pathway. Tether retains blacklist authority
over the underlying USDT on Ethereum.

## Type-specific risks

See `types/messaging.md` for base risk profile.

## Deployment divergence

Each chain OFT contract is deployed and configured independently; DVN thresholds,
executor assignments, and block confirmation requirements can diverge across chains.
Arbitrum adds sequencer dependency for timely message inclusion. A misconfiguration
on one chain (e.g., single-DVN mode) does not propagate to others but creates an
inconsistent security posture that is difficult to audit holistically.
