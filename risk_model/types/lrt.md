---
id: lrt
name: Liquid Restaking Token
description: LST variant where underlying ETH is additionally restaked via EigenLayer/Symbiotic.
parent_type: lst
examples: [kelp_rseth, renzo_ezeth, etherfi_weeth, puffer_pufeth, swell_rsweth]
key_risks:
  - validator_avs_slashing
  - avs_operator_risk
  - withdrawal_queue_delay
  - exchange_rate_vs_market_depeg
  - deep_chain_lrt
  - bridge_dep
  - quoted_vs_underlying_depeg
  - underlying_protocol_pause
  - concentrated_pool_dependency
  - per_deployment_profile_divergence
key_parameters:
  - avs_selection_criteria
  - slashing_insurance_coverage
  - max_avs_count
  - operator_delegation_strategy
  - bridge_type_for_l2_deployments
key_invariants:
  - "exchange_rate = (staked_eth + avs_rewards - slashing_losses) / total_lrt_supply"
  - "avs_slashing_risk per operator <= operator_stake_share"
  - "L2_bridged_supply <= L1_locked_lrt  (backing integrity)"
attack_patterns:
  - withdrawal_queue_blocking_lst
  - emode_correlation_engineering
---

## Mechanism

User deposits ETH → protocol stakes via LST (Lido/Rocket) → additionally
delegates to EigenLayer operators → operators run AVS (Actively Validated Services).
LRT represents claim on ETH + LST staking rewards + AVS rewards.
Additional slash risk: EigenLayer slashing conditions per AVS.

## Type-specific risk profile

### 4-layer dependency stack
```
LRT holder
  └── LRT protocol (Kelp/Renzo)
        └── EigenLayer (restaking layer)
              └── Validators (Ethereum PoS)
                    └── AVS operators (per-service)
```
Each layer has independent slashing conditions. Layer n failure
propagates upward.

### AVS slashing is new territory (2024-2025)
EigenLayer slashing was not live until 2024. The economic parameters of AVS
slashing conditions are being discovered in production. Over-aggressive AVS
slashing conditions can drain restaker capital rapidly.

### Cross-chain bridging adds backing risk
Most LRTs bridge to L2 via LayerZero OFT or similar. This creates the
exact rsETH/LayerZero vulnerability: L2 supply != L1 backing if bridge
is compromised. LRT on L2 = LST risk + EigenLayer risk + bridge risk.

### Multiple LRTs share EigenLayer
rsETH, ezETH, weETH all restake via EigenLayer. An EigenLayer-level event
(systemic bug, mass slashing) hits ALL LRTs simultaneously → correlated depeg
of entire LRT basket.

### Operator selection concentration
LRT protocols select EigenLayer operators. Concentrated delegation to few
operators = correlated slashing risk if those operators run same AVS with bug.
