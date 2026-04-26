---
id: cdp
name: CDP (Collateralized Debt Position)
description: Protocol mints its own stablecoin against user-posted collateral.
examples: [makerdao, liquity, crvusd, gho, prisma, raft]
key_risks:
  - oracle_staleness
  - thin_liquidity_source_manipulation
  - soft_peg_algo_failure
  - hard_peg_redemption_window_closed
  - psm_facilitator_imbalance
  - bad_debt_socialization
  - liquidation_bonus_too_small
  - governance_hostile_decision
  - reserve_composition_drift
  - native_stablecoin_peg_stress
key_parameters:
  - collateralization_ratio
  - stability_fee
  - liquidation_ratio
  - debt_ceiling
  - savings_rate
  - peg_stability_module_params
  - liquidation_penalty
key_invariants:
  - "collateral_value * collateral_ratio >= minted_debt"
  - "total_minted <= debt_ceiling"
  - "stablecoin_price ≈ $1 (via PSM or redemption arb)"
  - "global_collateral_ratio > min_ratio"
attack_patterns:
  - deleveraging_telegraph_frontrun
  - flash_governance
  - forced_selling_cascade_collateral
---

## Mechanism

Protocol mints stablecoin when users lock collateral. Maintains peg through:
- Redemption: anyone can redeem stablecoin for $1 of collateral
- PSM (Peg Stability Module): swap stablecoin ↔ other stables at 1:1
- Stability fee: borrowing rate that controls supply
- Emergency shutdown: winds down entire system if peg fails critically

## Type-specific risk profile

### Peg complexity
CDP stablecoin peg relies on a network of mechanisms, each with its own failure mode:
- PSM relies on deep reserves of accepted stables (USDC-risk)
- Redemption arbitrage relies on willing redeemers and liquid collateral
- Stability fee adjustment is slow (governance-gated)

### Collateral quality → peg quality
CDP is only as good as its weakest collateral. DAI backed heavily by USDC
means USDC depeg = DAI depeg (USDC/SVB March 2023: DAI briefly de-pegged).
Collateral diversification improves peg resilience but adds oracle surface.

### Governance-controlled parameters
All key parameters (stability fee, collateral types, debt ceilings) require
governance. Slow governance response during stress events = outdated parameters.
Liquity removed governance entirely — tradeoff: fixed params vs responsiveness.

### Death spiral risk
If collateral value drops sharply + liquidations don't clear fast enough →
stablecoin loses backing → peg breaks → collateral worth less (if protocol
token used) → more peg break. UST was extreme version; any CDP is susceptible
at lesser magnitude.
