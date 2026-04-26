---
slug: tornado_cash
name: Tornado Cash
types: []
deployments:
  - chain: ethereum
    tvl_usd: 570000000
    since: 2019-08-01
    note: "Primary deployment; OFAC-sanctioned Aug 2022. Immutable core contracts (v1/v2); Nova contracts upgradeable"
  - chain: bnb
    tvl_usd: 0
    since: 2021-06-01
    note: "Deployed but largely dormant post-sanctions"
  - chain: polygon
    tvl_usd: 0
    since: 2021-09-01
    note: "Deployed but largely dormant post-sanctions"
  - chain: avalanche
    tvl_usd: 0
    since: 2021-11-01
    note: "Deployed but largely dormant post-sanctions"
dependencies:
  - id: ethereum_zk_circuit
    type: cryptographic_primitive
    scope: [ethereum]
    note: "Groth16 ZK-SNARK circuit (Tornado core); trusted setup ceremony — compromise of ceremony would break privacy, not funds"
  - id: relayer_network
    type: infrastructure
    scope: [ethereum]
    note: "Anonymous relayers submit withdrawal transactions on behalf of users; relayers can front-run or censor but cannot steal funds from immutable contracts"
  - id: torn_governance
    type: governance
    scope: [ethereum]
    note: "TORN token governance — attacked in May 2023; attacker gained full control of governance vault"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "May 2023 governance attack: attacker submitted malicious proposal that appeared benign but included a hidden self-delegation of 1.2M TORN votes, granting full control of the governance vault. Attacker drained 483K TORN (~$2.1M) before community regained partial control via emergency patch. Governance remains structurally vulnerable to the same attack vector."
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "Tornado Cash Nova (cross-chain version) was deployed with upgradeable proxy contracts. Compromise of the upgrade key allows modification of Nova logic — unlike the immutable v1/v2 pools which have no admin surface. Nova deposits are at higher risk than legacy pools."
audits: []
---

## Overview

Tornado Cash is a non-custodial ZK-based privacy mixer on Ethereum (and several other
chains) that allows users to break the on-chain link between deposit and withdrawal
addresses using Groth16 SNARK proofs. The core v1/v2 contracts are immutable. In
August 2022, OFAC sanctioned Tornado Cash smart contract addresses, making use by
US persons legally restricted. In May 2023, the TORN governance contract was exploited
via a malicious proposal that granted an attacker full voting control and allowed
draining the governance vault. The protocol has no team-controlled upgrade path on
legacy pools; TVL remains locked in immutable contracts despite sanctions.

## Type-specific risks

Not classified under standard DeFi type taxonomy (privacy mixer). Standard type risk
files do not apply.

## Deployment divergence

Ethereum is the primary deployment by TVL. BNB, Polygon, and Avalanche deployments
are largely inactive post-sanctions. The critical governance attack surface exists
only on Ethereum (where TORN governance and the Nova upgradeable contracts live).
Legacy v1/v2 fixed-denomination pools on all chains are immutable — the only risk
is at the governance and Nova contract layer.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Core contract upgradeability | Immutable (v1/v2 pools) |
| Nova upgradeability | Upgradeable proxy (admin key risk) |
| Governance token | TORN |
| Governance attack | May 2023 — attacker gained 1.2M TORN votes via malicious proposal |
| OFAC sanctions | Aug 2022 — smart contract addresses sanctioned |
| ZK circuit | Groth16 (trusted setup ceremony, Powers of Tau) |
| Relayer censorship risk | Relayers can censor but cannot steal from immutable pools |
