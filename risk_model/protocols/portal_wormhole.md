---
slug: portal_wormhole
name: Portal (Wormhole)
types: [bridge, messaging]
deployments:
  - chain: ethereum
    tvl_usd: 1700000000
    since: 2021-08-01
  - chain: solana
    tvl_usd: 0
    since: 2021-08-01
    note: "Solana is message origin/destination; TVL is counted on Ethereum lock-side"
  - chain: bnb
    tvl_usd: 0
    since: 2022-01-01
  - chain: polygon
    tvl_usd: 0
    since: 2022-01-01
  - chain: avalanche
    tvl_usd: 0
    since: 2022-03-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2022-09-01
  - chain: optimism
    tvl_usd: 0
    since: 2022-09-01
  - chain: base
    tvl_usd: 0
    since: 2023-08-01
dependencies:
  - id: wormhole_guardians
    type: signing_committee
    scope: all_deployments
    note: "19-guardian network; 13/19 threshold required to sign VAAs (Verified Action Approvals); guardian set controlled by Wormhole Foundation"
  - id: wormhole_foundation
    type: governance
    scope: all_deployments
    note: "Controls guardian set membership and protocol upgrade authority"
  - id: chain_endpoints
    type: smart_contract
    scope: all_deployments
    note: "Per-chain endpoint contracts (Core Bridge) handle lock/mint and burn/unlock logic"
active_risks:
  - risk_id: guardian_key_leak
    deployment: all
    note: "The 13/19 guardian threshold is the sole cryptographic security guarantee; compromise of 13 guardian keys (via social engineering, infrastructure breach, or insider) allows forging arbitrary VAAs — replicating the Feb 2022 exploit vector. Jump Crypto rescued that incident ($320M) but no equivalent backstop is guaranteed"
  - risk_id: bridged_backing_loss
    deployment: all
    note: "Portal uses a lock-and-mint model; wrapped tokens on destination chains are claims on assets locked in source-chain vaults. An exploit on any supported chain's endpoint contract can drain locks without burning wrapped supply, destroying peg"
  - risk_id: bridge_pause_censorship
    deployment: all
    note: "Wormhole Foundation controls guardian set membership; removal or replacement of guardians can be executed unilaterally, effectively pausing the bridge for specific routes or globally"
  - risk_id: proxy_upgrade_authority
    deployment: all
    note: "Core Bridge contracts on each chain are upgradeable proxies; upgrade authority is held by Wormhole Foundation multisigs with varying timelock configurations per chain"
  - risk_id: per_deployment_divergence
    deployment: all
    note: "Each chain's endpoint contract is independently deployed and may have divergent upgrade schedules, guardian-set sync delays, and rate-limit configurations — creating windows where one chain's state is inconsistent with others"
audits:
  - firm: Trail of Bits
    date: 2022-01
    url: ""
  - firm: Neodyme
    date: 2022-03
    url: ""
  - firm: OtterSec
    date: 2022-06
    url: ""
  - firm: OtterSec
    date: 2022-09
    url: ""
  - firm: Kudelski
    date: 2022-11
    url: ""
  - firm: Certik
    date: 2023-01
    url: ""
  - firm: Certik
    date: 2023-04
    url: ""
  - firm: Zellic
    date: 2023-06
    url: ""
  - firm: Zellic
    date: 2023-09
    url: ""
  - firm: Trail of Bits
    date: 2023-11
    url: ""
  - firm: Neodyme
    date: 2024-01
    url: ""
  - firm: OtterSec
    date: 2024-02
    url: ""
  - firm: Cyfrin
    date: 2024-04
    url: ""
  - firm: Zellic
    date: 2024-05
    url: ""
  - firm: Trail of Bits
    date: 2024-06
    url: ""
  - firm: OtterSec
    date: 2024-07
    url: ""
  - firm: Neodyme
    date: 2024-08
    url: ""
  - firm: Zellic
    date: 2024-09
    url: ""
  - firm: Certik
    date: 2024-10
    url: ""
  - firm: Trail of Bits
    date: 2024-11
    url: ""
  - firm: OtterSec
    date: 2024-12
    url: ""
  - firm: Kudelski
    date: 2025-01
    url: ""
  - firm: Zellic
    date: 2025-02
    url: ""
  - firm: Neodyme
    date: 2025-03
    url: ""
---

## Overview

Portal is the token bridge product built on the Wormhole cross-chain messaging protocol.
Wormhole's security model relies on 19 Guardians — a permissioned set of validators operated
by ecosystem participants — who observe and co-sign cross-chain messages (VAAs). A 13/19 supermajority
is required to produce a valid VAA, which endpoint contracts on each chain verify before
processing bridge transfers. In February 2022, a signature verification bug on the Solana endpoint
allowed an attacker to forge a VAA and mint 120,000 wETH (~$320M) without locking collateral;
Jump Crypto backstopped the loss.

## Type-specific risks

See `types/bridge.md` and `types/messaging.md` for base risk profiles.

## Deployment divergence

Each chain's Core Bridge contract is independently deployed and upgraded. Guardian-set updates
propagate chain-by-chain and can lag behind the canonical set for hours, creating inconsistent
security thresholds across routes. Solana endpoint has historically been the highest-risk surface
(2022 exploit). Rate limits and per-chain caps differ per deployment.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Guardian set size | 19 |
| Signing threshold | 13/19 |
| Guardian selection | Wormhole Foundation |
| Bridge model | Lock-and-mint (lock on source, mint wrapped on destination) |
| Upgrade authority | Wormhole Foundation multisig (per-chain timelock varies) |
| Notable incident | Feb 2022 — $320M signature bypass on Solana; rescued by Jump Crypto |
