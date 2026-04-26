---
id: avalanche
name: Avalanche C-Chain
vm: evm
consensus: snowman_pos
layer: L1
sequencer: null
validator_count: ~1600
validator_stake_token: AVAX
finality_seconds: ~1
l1: null
native_bridge: avalanche_bridge
key_risks:
  - chain_reorg
  - rpc_infra_dep
  - bridge_dep
  - governance_signer_key_leak
risk_notes:
  finality: >
    Avalanche consensus reaches probabilistic finality very quickly (~1 sec),
    but this is not cryptographic finality as in Ethereum post-Merge. Under certain
    network conditions finality may be delayed.
  validator_count: >
    ~1600 validators — more decentralized than BSC/Polygon PoS, but
    stake concentration in large operators (Ava Labs, large staking pools)
    remains a concern.
  bridge_dep: >
    Avalanche Bridge (AB) is based on Intel SGX and an 8-of-8 multisig. SGX-based
    security is a specific threat model: side-channel attacks on SGX.
notable_incidents: []
defi_context:
  notes: >
    Aave V3, Benqi, Trader Joe. AVAX as collateral in lending protocols.
    Avalanche subnets are architecturally isolated from C-Chain risks.
    Main DeFi on C-Chain.
---

## Chain-specific risk profile

Avalanche C-Chain is an EVM-compatible chain with Snowman consensus. Main
differences from Ethereum: faster finality, different validator economics.

## SGX bridge risk

Avalanche Bridge uses Intel SGX for key management. SGX has a history of
side-channel vulnerabilities (Spectre, Plundervolt). This is a non-standard
threat model for bridge security.

## Subnet isolation

Avalanche subnets are separate chains with their own validators and rules.
DeFi protocols on subnets have a different risk profile than C-Chain protocols.
Gateway between subnet and C-Chain = additional bridge surface.
