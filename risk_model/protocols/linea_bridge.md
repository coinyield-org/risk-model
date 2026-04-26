---
slug: linea_bridge
name: Linea Bridge (ConsenSys)
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 380000000
    since: 2023-07-01
  - chain: linea
    tvl_usd: 0
    since: 2023-07-01
dependencies:
  - id: linea_sequencer
    type: operator
    scope: all_deployments
    note: ConsenSys single centralized sequencer
  - id: linea_zk_prover
    type: zk_proof_system
    scope: all_deployments
    note: custom zkEVM proof system
  - id: consensys_governance
    type: governance
    scope: all_deployments
active_risks:
  - risk_id: sequencer_downtime
    note: "ConsenSys operates a single sequencer; demonstrated Feb 2025 — chain was voluntarily paused to block Bybit hack funds movement, proving unilateral halt capability"
  - risk_id: proxy_upgrade_authority
    note: "ConsenSys multisig holds proxy upgrade authority over bridge contracts; no long timelock observed"
  - risk_id: bridge_pause_censorship
    note: "Bridge admin can pause asset flow; Feb 2025 incident confirms willingness to exercise this power unilaterally"
  - risk_id: deployer_key_leak
    note: "ConsenSys multisig compromise would allow arbitrary bridge upgrades and potential fund extraction"
audits:
  - firm: Cyfrin
    date: 2024-01
    url: ""
---

## Overview

Linea Bridge is the canonical L1-to-L2 bridge connecting Ethereum to the Linea zkEVM
L2, operated by ConsenSys. TVL (~$0.38B) represents ETH and ERC-20 assets locked on
Ethereum backing Linea activity. Eight Cyfrin audit reports are indexed. In February
2025, ConsenSys voluntarily paused the Linea chain to prevent movement of $1.5B in
funds stolen in the Bybit exchange hack — a real-world demonstration that the bridge
and chain can be halted unilaterally by a single organization.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Deployment divergence

Bridge state is maintained across Ethereum (lock side) and Linea (mint side).
ZK proof finality adds a delay between L2 execution and L1 withdrawal availability.
All governance actions originate from ConsenSys-controlled multisig with no
equivalent of a decentralized DAO or long timelock for security-critical changes.
