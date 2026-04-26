---
slug: stacks_sbtc
name: Stacks sBTC
types: [bridge]
deployments:
  - chain: bitcoin
    tvl_usd: 320000000
    since: 2024-01-01
    note: "BTC is locked on Bitcoin mainnet by the sBTC signer network; sBTC is minted on the Stacks L2"
dependencies:
  - id: stacks_pox
    type: consensus
    scope: [bitcoin]
    note: "Stacks uses Proof of Transfer (PoX) anchored to Bitcoin; Stacks blocks are produced by STX stackers who transfer BTC to Bitcoin miners"
  - id: sbtc_signer_network
    type: signing_committee
    scope: [bitcoin]
    note: "sBTC signers collectively control the BTC wallet that holds all locked Bitcoin; a threshold of signers must approve mint/burn operations"
  - id: stacks_foundation
    type: governance
    scope: [bitcoin]
    note: "Stacks Foundation governs protocol upgrades, signer set membership, and emergency procedures"
active_risks:
  - risk_id: guardian_key_leak
    deployment: bitcoin
    note: "The sBTC signer network controls the Bitcoin multisig wallet holding all locked BTC; compromise of a threshold of signer keys via social engineering, infrastructure breach, or insider threat would allow unauthorized withdrawal of the entire BTC reserve — the same attack vector as the Wormhole guardian compromise pattern"
  - risk_id: bridge_lock_backing_loss
    deployment: bitcoin
    note: "sBTC uses a lock-and-mint model: BTC is locked in a signer-controlled wallet and sBTC is minted on Stacks; a consensus failure among signers, a key compromise, or a bug in the signer coordination protocol could result in locked BTC being inaccessible or transferred without corresponding sBTC burning"
  - risk_id: deployer_key_leak
    deployment: bitcoin
    note: "Stacks Clarity contracts (no EVM; Stacks-native language) have not been covered by indexed audit reports; contract upgrade authority held by the Stacks Foundation represents an unverified attack surface for the sBTC minting and redemption logic"
  - risk_id: chain_halt
    deployment: bitcoin
    note: "Stacks L2 has a limited operational track record and a smaller validator/stacker set than mature L2s; a consensus failure or PoX mechanism breakdown halts sBTC minting, burning, and transfers, trapping BTC in the locked wallet with no settlement path until the chain recovers"
audits: []
---

## Overview

Stacks sBTC is a decentralized wrapped Bitcoin operating on the Stacks Layer 2, which
is anchored to Bitcoin via the Proof of Transfer (PoX) consensus mechanism. BTC is locked
in a threshold-multisig wallet controlled by the sBTC signer network; in exchange, sBTC is
minted on the Stacks chain. Unlike custodial wrapped BTC products, sBTC aims for
trustless operation through cryptographic threshold signing. However, the signer network
is permissioned, creating a signing committee security model analogous to Wormhole's
guardian set, with the signer threshold as the primary trust assumption.

## Type-specific risks

See `types/bridge.md` for base risk profile.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Locking mechanism | Signer-controlled Bitcoin multisig (threshold) |
| Minting chain | Stacks L2 (Clarity VM) |
| Bitcoin settlement | PoX — Stacks blocks anchored to Bitcoin |
| Signer selection | Permissioned by Stacks governance |
| Audit coverage | None in indexed PDFs (Clarity contracts) |
| Comparable model | Wormhole guardian set (13/19 threshold) |
