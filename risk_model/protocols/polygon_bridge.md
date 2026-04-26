---
slug: polygon_bridge
name: Polygon POS Bridge
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 2600000000
    since: 2020-06-01
    note: "L1 lock side on Ethereum; canonical PoS bridge for Polygon mainnet"
dependencies:
  - id: polygon_pos_validators
    type: validator_set
    scope: all_deployments
    note: "~100 validators checkpoint Ethereum roughly every 30 minutes via Heimdall nodes"
  - id: heimdall
    type: checkpoint_layer
    scope: all_deployments
    note: "Heimdall nodes are responsible for checkpointing Polygon state roots to Ethereum"
  - id: polygon_team
    type: governance
    scope: all_deployments
    note: "Polygon team controls upgrade keys for bridge proxy contracts via multisig"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    note: "Indirect dependency via assets bridged and protocols built on top"
active_risks:
  - risk_id: bridge_signing_committee
    deployment: ethereum
    note: "The Polygon PoS bridge relies on ~100 validators checkpointing Ethereum via a 2/3 supermajority. This validator set is substantially smaller and less decentralized than Ethereum consensus. A supermajority colluding or being coerced could submit fraudulent state roots."
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "Polygon team controls a multisig with upgrade authority over the bridge proxy contracts on Ethereum. A compromised or coerced multisig can modify the bridge implementation and drain the $2.6B L1 escrow. This authority was silently exercised in December 2021 to patch a $24B vulnerability."
  - risk_id: guardian_key_leak
    deployment: ethereum
    note: "The bridge guardian/admin key, if compromised, allows pause and potential redirection of bridged assets. The March 2022 $2M exploit demonstrated that bridge contracts can be targeted."
  - risk_id: whale_concentration
    deployment: ethereum
    note: "MATIC/POL validator stake is concentrated among a small number of institutional validators. Top 10 validators control a disproportionate share of checkpointing power, reducing the practical cost of collusion."
audits:
  - firm: Sigma Prime
    date: 2021-05
    url: ""
  - firm: Halborn
    date: 2021-09
    url: ""
  - firm: Trail of Bits
    date: 2022-03
    url: ""
---

## Overview

The Polygon PoS Bridge is the canonical bridge connecting Ethereum to Polygon PoS.
Assets are locked in an L1 escrow on Ethereum and minted on Polygon PoS. Security
relies on a set of ~100 validators who periodically checkpoint Polygon state to
Ethereum via the Heimdall layer. In December 2021, Polygon silently patched a
$24B vulnerability via an emergency hard fork. In March 2022, a $2M exploit occurred
on the PoS bridge itself.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Unlike OP Stack bridges (which use fraud proofs or validity proofs), the Polygon PoS
bridge uses a validator-committee checkpoint model. This introduces a distinct trust
model: users trust that 2/3+ of the validator set is honest, rather than trusting
cryptographic proofs. The upgrade key risk is particularly material given the
December 2021 silent fix precedent.
