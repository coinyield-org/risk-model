---
id: bridge
name: Cross-Chain Bridge
description: Moves assets between chains by locking on source and minting on destination.
examples: [wormhole, across, stargate, synapse, hop, cbridge, polygon_pos_bridge]
key_risks:
  - bridge_lock_backing_loss
  - bridge_pause_censorship
  - guardian_key_leak
  - proxy_upgrade_authority
  - canonical_vs_bridged_coexistence
  - per_deployment_profile_divergence
  - message_replay_ordering
  - chain_reorg
key_parameters:
  - signing_committee_size
  - signing_threshold
  - fraud_proof_window
  - liquidity_pool_size
  - fee_structure
  - rate_limits
key_invariants:
  - "locked_on_source == minted_on_destination  (backing integrity)"
  - "total_bridged_supply <= lock_contract_balance"
  - "msg_nonce unique per chain pair"
attack_patterns:
  - withdrawal_queue_blocking_lst
---

## Trust model taxonomy

Bridges differ fundamentally in their trust model:

| Type | Trust assumption | Example |
|------|-----------------|---------|
| Native/rollup bridge | L1 consensus security | Arbitrum bridge |
| Optimistic bridge | 1 honest watcher in challenge window | Across |
| MPC/multisig | Threshold of signers honest | Wormhole (19-of-19) |
| Liquidity network | Relayers + LP economics | Hop |
| ZK bridge | Validity proof (most trust-minimized) | Starkgate |

## Type-specific risk profile

### Signing committee = biggest attack surface
MPC/multisig bridges: if attacker controls >= threshold signers, can sign
arbitrary messages. Wormhole Feb 2022 ($320M) was not signer compromise but
signature verification bug — but result same: unauthorized mint on destination.

### Asymmetric finality risk
Source chain may reorg after bridge confirms message. If source tx reverts
but destination already minted → double-spend. Bridge must wait for finality
of source chain before finalizing destination mint.

### Rate limiting as incomplete protection
Some bridges have per-period rate limits (max transfer per hour). This limits
single-tx exploit but doesn't prevent multi-tx drain over time. Limits also
block legitimate large transfers during high usage.

### Canonical fragmentation
Multiple bridges serving same asset pair (USDC via Wormhole, Circle CCTP,
native L2 bridge) → multiple "USDC" contracts with different backing levels.
Protocol accepting any of them assumes equal risk — they're not equal.
