---
slug: bedrock
name: Bedrock uniBTC
types: [bridge, lrt]
deployments:
  - chain: ethereum
    tvl_usd: 210000000
    since: 2024-03-01
  - chain: arbitrum
    tvl_usd: 80000000
    since: 2024-05-01
  - chain: bnb
    tvl_usd: 40000000
    since: 2024-06-01
  - chain: ethereum
    tvl_usd: 20000000
    since: 2024-07-01
    note: "Merlin Chain TVL is included in aggregated estimates; Merlin is a Bitcoin L2"
dependencies:
  - id: babylon_protocol
    type: restaking_protocol
    scope: all_deployments
    note: "Bedrock integrates with Babylon Protocol for BTC staking; Babylon provides the native BTC staking security layer that backs uniBTC yield"
  - id: bedrock_team
    type: custodian
    scope: all_deployments
    note: "Bedrock acts as the custodian/bridge operator for underlying BTC; uniBTC is minted against BTC held or delegated by the Bedrock team"
  - id: multichain_bridge
    type: bridge
    scope: [arbitrum, bnb]
    note: "uniBTC on Arbitrum and BNB Chain is bridged from Ethereum; bridge integrity is a prerequisite for backing validity on non-Ethereum chains"
active_risks:
  - risk_id: custodian_risk
    deployment: all
    note: "Bedrock holds or delegates the underlying BTC used to mint uniBTC; the protocol relies on the Bedrock team's operational integrity for custody. Unlike WBTC (BitGo) or cbBTC (Coinbase), Bedrock does not have an established custodial track record, making this the primary risk vector"
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "Babylon Protocol integration introduces BTC restaking slashing risk; BTC validators staking via Babylon can be slashed for double-signing, and that slashing event reduces the backing behind uniBTC proportionally"
  - risk_id: bridge_lock_backing_loss
    deployment: [arbitrum, bnb]
    note: "uniBTC on Arbitrum and BNB Chain is backed by a bridge lock on Ethereum; a smart contract exploit or bridge operator failure on the cross-chain bridge invalidates the backing of all non-Ethereum uniBTC without recourse"
  - risk_id: deployer_key_leak
    deployment: all
    note: "Bedrock smart contracts have PeckShield audits, but upgrade authority and mint/burn control remain with the Bedrock team multisig; compromise of that multisig allows unauthorized uniBTC minting, diluting backing for all holders"
  - risk_id: per_deployment_divergence
    deployment: [arbitrum, bnb]
    note: "Each chain's uniBTC deployment has a different bridge mechanism and security assumption; Ethereum deployment has direct Bedrock/Babylon custody, while Arbitrum and BNB Chain deployments add a bridge layer with separate attack surface and liquidity depth"
audits:
  - firm: PeckShield
    date: 2024-04
    url: ""
  - firm: PeckShield
    date: 2024-07
    url: ""
  - firm: PeckShield
    date: 2024-10
    url: ""
---

## Overview

Bedrock uniBTC is a wrapped BTC token that integrates with Babylon Protocol to provide
native BTC staking yield. Users deposit BTC (or WBTC) and receive uniBTC, which accrues
Babylon staking rewards. uniBTC is deployed across Ethereum, Arbitrum, BNB Chain, and
Merlin Chain (Bitcoin L2), with cross-chain copies bridged from Ethereum. Bedrock acts
as both the bridge operator and the custodial/delegation layer between user BTC and
Babylon's staking infrastructure.

## Type-specific risks

See `types/bridge.md` and `types/lrt.md` for base risk profiles.

## Deployment divergence

Ethereum is the canonical deployment where BTC custody and Babylon delegation occur.
Arbitrum and BNB Chain hold bridged uniBTC with no direct BTC custody on those chains —
backing validity depends entirely on the bridge integrity. Merlin Chain (Bitcoin L2)
adds a further layer of Bitcoin L2 trust assumptions on top of the Bedrock/Babylon stack.
