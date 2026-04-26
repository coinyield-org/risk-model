---
id: centrifuge
name: Centrifuge Chain
vm: substrate
consensus: polkadot_parachain
layer: appchain
sequencer: null
finality_to_l1: polkadot_relay_chain_finality
l1: polkadot_relay_chain
native_bridge: polkadot_xcm
key_risks:
  - chain_halt
  - chain_reorg
  - bridge_dep
  - rpc_infra_dep
  - governance_signer_key_leak
risk_notes:
  chain_halt: >
    Centrifuge-specific liveness depends on parachain block production,
    relay-chain inclusion, collators, and XCM availability.
  chain_reorg: >
    Finality is inherited from the Polkadot relay chain. Before finality,
    parachain state can be reorganized like other relay-chain-secured systems.
  bridge_dep: >
    Most DeFi liquidity for Centrifuge assets lives outside the native chain,
    so XCM and Ethereum bridge paths are structural dependencies.
  rpc_infra_dep: >
    RWA workflows depend heavily on indexers, off-chain reporting, and
    application-specific infrastructure.
defi_context:
  notes: >
    Centrifuge is an RWA-focused appchain. Risk is dominated by issuer,
    legal-structure, bridge, and data availability assumptions rather than
    high-frequency on-chain liquidation mechanics.
---

## Chain-specific risk profile

Centrifuge Chain is a Substrate/Polkadot appchain used primarily for RWA
issuance and asset administration.

## RWA-specific chain risk

The chain is only one layer. RWA positions also depend on SPVs, asset
originators, reporting, legal enforceability, and off-chain payment flows.

## Bridge and liquidity path

When Centrifuge assets are consumed by Ethereum DeFi, the operational path goes
through bridge/XCM/accounting layers. That bridge path should be modeled
separately from the issuer credit risk.

