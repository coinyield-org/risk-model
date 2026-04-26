---
id: hyperliquid_l1
name: Hyperliquid L1
vm: hyperliquid_custom
consensus: proprietary_pos
layer: L1
sequencer: hyperliquid_validators
sequencer_type: validator_ordered
l1: null
native_bridge: hyperliquid_bridge
key_risks:
  - chain_halt
  - operator_concentration
  - governance_hostile_decision
  - rpc_infra_dep
  - bridge_dep
risk_notes:
  chain_halt: >
    A halt or validator coordination failure freezes trading, withdrawals,
    oracle updates, liquidations, and vault operations for protocols deployed
    on Hyperliquid L1.
  operator_concentration: >
    Validator/operator set maturity and distribution are core assumptions for
    a newer vertically integrated L1.
  governance_hostile_decision: >
    Protocol and chain governance are tightly coupled. Parameter, listing, and
    risk-engine decisions can have system-wide effects.
  bridge_dep: >
    External asset ingress/egress depends on bridge and exchange integration
    paths, not only on L1 consensus.
defi_context:
  notes: >
    Hyperliquid L1 is strongly tied to the Hyperliquid trading venue, HLP vault,
    and perps/liquidation engine. Cascade risk is market-microstructure-heavy.
---

## Chain-specific risk profile

Hyperliquid L1 is a newer vertically integrated chain/venue environment. The
main risk is not only base-chain consensus; it is the coupling between chain
liveness, exchange risk engine, liquidations, and vault counterparties.

## Market-structure coupling

If the chain or matching/risk engine is unavailable during market volatility,
positions cannot be managed while external prices continue moving.

## Bridge and venue dependency

Deposits, withdrawals, and collateral quality depend on bridge/venue operations.
This should be modeled as both chain risk and protocol-level dependency risk.

