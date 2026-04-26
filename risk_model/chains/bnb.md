---
id: bnb
name: BNB Smart Chain (BSC)
vm: evm
consensus: pos_parlia
layer: L1_adjacent
sequencer: null
validator_count: 21_active
validator_stake_token: BNB
finality_seconds: ~3
l1: null
native_bridge: bnb_bridge
trust_model: highly_centralized_validator_set
key_risks:
  - chain_reorg
  - governance_signer_key_leak
  - bridge_dep
  - rpc_infra_dep
  - mempool_censorship_infra
risk_notes:
  validator_count: >
    21 active validators (PoSA) — the most centralized of the large EVM chains.
    All validators are whitelisted by Binance. A >50% attack requires compromising 11 validators.
    This is not theory — validators operationally depend on Binance corp.
  bridge_dep: >
    BNB Bridge was hacked in October 2022 ($586M). Attacker forged a Merkle proof
    for BSC Token Hub. Largest bridge exploit in history.
    Shows: centralized chain → centralized bridge → catastrophic failure.
  chain_reorg: >
    21 validators → reorg is easier than on Ethereum. BSC has a history of short
    reorgs. Protocols must wait several blocks before finality.
  governance_signer_key_leak: >
    Binance as de-facto chain operator has override capability via
    governance contracts. Their compliance with regulators = chain compliance.
notable_incidents:
  - date: 2022-10-07
    description: >
      BSC Token Hub Bridge exploit: $586M. Vulnerability in IAVL tree Merkle proof
      verification. Binance temporarily halted the chain — a precedent of unilateral chain halt.
  - date: 2022-10-06
    description: >
      BNB chain halt for a patch after the bridge exploit. 21 validators were sent
      a request to halt the chain via Binance coordination. The chain was halted
      in ~30 minutes. Demonstrates the degree of centralized control.
defi_context:
  notes: >
    Venus, PancakeSwap, Lista DAO. Historically high frequency of flash loan
    exploits on BSC due to affordable block building and thin liquidity of assets.
    BSC DeFi is considered a higher risk baseline compared to Ethereum/L2.
---

## Chain-specific risk profile

BSC is the most centralized of the large EVM chains. 21 validators, all
selected by Binance. It is fast and cheap, but trust assumptions are fundamentally
different from Ethereum.

## Chain halt precedent

After the BSC bridge exploit, Binance coordinated halting the chain among 21
validators in ~30 minutes. This shows: BSC can be halted at the will of
Binance/validators. For DeFi protocols this is unilateral pause risk.

## Flash loan exploit ecosystem

BSC historically has a higher rate of flash loan exploits than Ethereum:
- Cheap tx → cheaper to run complex multi-step attacks
- Thin liquidity on most BSC-native assets
- Lower auditing standards among many BSC-native protocols
