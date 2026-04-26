---
slug: base_bridge
name: Base Bridge (Canonical)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 2800000000
    since: 2023-08-09
    note: "L1 lock side; assets locked on Ethereum, minted on Base"
dependencies:
  - id: coinbase
    type: sequencer_operator
    scope: all_deployments
    note: "Coinbase operates the Base sequencer; single point of liveness and ordering control"
  - id: op_stack
    type: bridge_framework
    scope: all_deployments
    note: "OP Stack canonical bridge contracts; same implementation as Optimism bridge"
  - id: ethereum
    type: settlement_layer
    scope: all_deployments
    note: "Fraud proof window: 7-day challenge period for withdrawals back to L1"
  - id: circle
    type: issuer
    scope: all_deployments
    assets: [USDC]
active_risks:
  - risk_id: bridge_signing_committee
    deployment: ethereum
    note: "Base does not yet have a fully operational fault-proof system permitting trustless withdrawals. During this period, a privileged multisig (Coinbase/OP Labs controlled) can override dispute resolution, creating a committee-level trust assumption."
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "OP Stack bridge proxy contracts are upgradeable by the Security Council / Coinbase multisig. A malicious or coerced upgrade can redefine withdrawal logic and potentially drain the L1 escrow."
  - risk_id: guardian_key_leak
    deployment: ethereum
    note: "The Base Guardian role (Coinbase-controlled) can pause the bridge unilaterally; key compromise enables forced freeze of $2.8B in locked assets."
audits:
  - firm: ""
    date: ""
    url: ""
    note: "Same OP Stack contracts as coinbase_bridge; see coinbase_bridge.md for audit references"
---

## Overview

Base Bridge is the canonical OP Stack bridge connecting Ethereum mainnet to the Base
L2. Assets are locked in an L1 escrow contract and minted as equivalents on Base.
Withdrawals from Base to Ethereum require a 7-day challenge window. DefiLlama tracks
this as a separate TVL entry from the Coinbase-branded bridge, but the underlying
smart contracts are identical OP Stack deployments.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

This entry shares on-chain contracts with `coinbase_bridge`. The DefiLlama TVL split
is an accounting artifact — both entries represent the same L1 escrow. Risk analysis
should be consolidated with `coinbase_bridge.md` to avoid double-counting.
