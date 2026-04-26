---
id: merlin_chain
name: Merlin Chain
vm: evm_bitcoin_l2
consensus: bitcoin_l2
layer: L2
sequencer: merlin_network
sequencer_type: centralized_or_committee
l1: bitcoin
native_bridge: merlin_bridge
key_risks:
  - sequencer_downtime
  - chain_halt
  - bridge_dep
  - rpc_infra_dep
  - governance_signer_key_leak
risk_notes:
  sequencer_downtime: >
    Merlin Chain execution depends on L2 operator/sequencer availability.
    Downtime can freeze DeFi operations while BTC and external markets move.
  bridge_dep: >
    BTC and other assets on Merlin depend on bridge/custody/accounting paths
    from Bitcoin and EVM chains. This dominates collateral backing risk.
  chain_halt: >
    As a newer Bitcoin L2, operational maturity and recovery procedures are key
    liveness assumptions.
  governance_signer_key_leak: >
    Bridge and upgrade controls can be controlled by limited signer or operator
    sets, making key compromise a chain-wide risk.
defi_context:
  notes: >
    Merlin Chain is treated as a Bitcoin L2 / EVM execution domain. DeFi risk
    is mostly bridge-backed BTC liquidity plus centralized operator assumptions.
---

## Chain-specific risk profile

Merlin Chain brings EVM-style DeFi to Bitcoin-linked assets. The dominant
cascade risk is bridge/custody backing rather than native Bitcoin settlement.

## Bitcoin L2 assumptions

Protocols should not treat Merlin assets as equivalent to native BTC. They
depend on L2 execution, bridge operators, and redemption paths.

## DeFi liquidity risk

Liquidity can be thin relative to bridged asset notional. A bridge pause or
confidence shock can create large discounts and withdrawal pressure.

