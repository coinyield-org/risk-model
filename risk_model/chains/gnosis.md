---
id: gnosis
name: Gnosis Chain
vm: evm
consensus: pos
layer: L1_sidechain
sequencer: null
l1: null
native_bridge: gnosis_bridge
key_risks:
  - chain_reorg
  - rpc_infra_dep
  - bridge_dep
  - mempool_censorship_infra
  - governance_signer_key_leak
risk_notes:
  chain_reorg: >
    Gnosis Chain has faster and cheaper execution than Ethereum but a smaller
    validator and economic security footprint. Protocols should not inherit
    Ethereum finality assumptions automatically.
  bridge_dep: >
    Most assets arrive through bridge paths from Ethereum or other chains.
    Bridge pause, message delay, or accounting mismatch can dominate protocol
    risk for bridged collateral.
  rpc_infra_dep: >
    Smaller chains often have thinner RPC/provider diversity. Liquidators and
    keepers are more exposed to endpoint outages.
  governance_signer_key_leak: >
    Chain and bridge administration paths include governance and multisig
    controls that can become chain-wide dependencies.
defi_context:
  notes: >
    Gnosis Chain is an EVM sidechain with meaningful stablecoin and payments
    usage. Risk model should treat it as a separate settlement domain, not as
    Ethereum-equivalent.
---

## Chain-specific risk profile

Gnosis Chain is EVM-compatible, but its security and liquidity profile differs
from Ethereum mainnet.

## Bridge-heavy asset base

Many assets on Gnosis are bridged. For DeFi risk, a Gnosis deployment may have
both chain liveness risk and bridge-backed asset risk at the same time.

## Operational dependency

RPC diversity, bridge operators, and governance/admin paths matter more than
raw contract composability for most Gnosis exposures in this model.

