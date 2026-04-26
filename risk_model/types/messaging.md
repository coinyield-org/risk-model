---
id: messaging
name: Cross-Chain Messaging Protocol
description: General-purpose cross-chain message passing; assets may or may not move.
examples: [layerzero, axelar, chainlink_ccip, wormhole_messaging, hyperlane]
key_risks:
  - bridge_lock_backing_loss
  - bridge_pause_censorship
  - message_replay_ordering
  - guardian_key_leak
  - proxy_upgrade_authority
  - per_deployment_profile_divergence
  - timelock_skew_cross_chain
  - oracle_provider_dep
key_parameters:
  - dvn_count
  - dvn_threshold
  - executor_config
  - message_library_version
  - endpoint_upgrade_authority
key_invariants:
  - "message delivered exactly once  (replay protection via nonce)"
  - "message content unmodified  (integrity)"
  - "delivery in order per pathway  (if ordered channel)"
  - "DVN threshold: >= required_dvns have confirmed"
attack_patterns: []
---

## Mechanism

OApp (Omnichain Application) sends message via endpoint on source chain.
DVNs (Decentralized Verifier Networks) observe source tx and attest to
destination. Executor delivers message when threshold attestations received.

## LayerZero DVN architecture (most relevant for DeFi)

```
Source chain:
  OApp.send() → LayerZero Endpoint → emit Packet event

DVN layer:
  N DVNs observe event → each signs attestation
  If M-of-N threshold met → message can be executed

Destination chain:
  Executor calls Endpoint.deliver() → OApp.lzReceive()
```

## Type-specific risk profile

### DVN configuration is per-OApp
Each OApp independently configures its DVN set and threshold.
Default config = LayerZero's default DVNs. Many developers ship with
default (smaller threshold) for cost savings.
Custom config = better security but requires active maintenance.

### DVN compromise = arbitrary message injection
If attacker controls >= threshold DVNs, can create valid attestations for
any message on any pathway. This is the canonical rsETH/LayerZero attack vector:
forge "burned on L2, unlock on L1" message → drain L1 lock contract.

### Endpoint upgrade authority
LayerZero endpoint contract is upgradeable. Endpoint upgrade = all OApps
on that chain affected simultaneously. Upgrade process is governance-gated
but creates a shared upgrade surface.

### Executor is separate from DVN
DVN attests to message validity. Executor submits the message on destination.
If executor fails (gas, downtime), message sits undelivered. Some OApps
implement automated retries; others require manual intervention.

### Nonce and replay protection
Cross-chain messages must have replay protection (nonce per pathway).
If nonce check is bypassable (out-of-order delivery mode), message can be
replayed or reordered — relevant for governance messages and token mints.
