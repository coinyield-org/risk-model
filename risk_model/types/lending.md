---
id: lending
name: Lending Protocol
description: Over-collateralized borrow/lend markets with liquidation mechanism.
examples: [aave_v3, compound_v3, morpho, spark, radiant]
key_risks:
  - oracle_staleness
  - thin_liquidity_source_manipulation
  - quoted_vs_underlying_depeg
  - utilization_full_bank_run
  - bad_debt_socialization
  - liquidation_bonus_too_small
  - liquidation_bonus_too_large
  - emode_correlation_break
  - single_keeper_dependency
  - gas_ddos_liquidation
  - supply_cap_mismatch
  - parameter_update_lag
  - downstream_protocol_failure
  - safety_module_slash_exposure
key_parameters:
  - ltv
  - liquidation_threshold
  - liquidation_bonus
  - supply_cap
  - borrow_cap
  - close_factor
  - reserve_factor
  - ir_curve_params
  - emode_category
  - isolation_mode_flag
  - debt_ceiling
key_invariants:
  - "sum(collateral_i * price_i * liqThreshold_i) >= sum(debt_j * price_j)"
  - "utilization = totalBorrows / totalSupply"
  - "liq_threshold > ltv  (always positive health buffer)"
  - "liquidation_bonus < (1 - liq_threshold)  (no instant bad debt on liq)"
attack_patterns:
  - keeper_bad_debt_siphon
  - gas_ddos_liquidation
  - withdrawal_queue_blocking_lst
  - emode_correlation_engineering
  - deleveraging_telegraph_frontrun
  - forced_selling_cascade_collateral
---

## Mechanism

Suppliers deposit assets → receive yield-bearing position tokens (aToken, cToken).
Borrowers post overcollateralized collateral → borrow against LTV.
When health factor < 1 → liquidators repay debt, receive collateral + bonus.
Interest rate adjusts by utilization kink curve.

## Type-specific risk profile

### Oracle dependency (structural)
Every single market has an oracle dependency. Bad oracle on one asset ≠ affects
only that market — it can drain cross-market liquidity if borrowers lever against
inflated collateral price.

### Liquidation economics
The system relies on economically rational third parties (liquidators). When:
- Bonus < gas cost → no liquidators → bad debt
- Bonus > collateral buffer → liquidation itself creates bad debt

Both failure modes co-exist depending on asset volatility and position size.

### E-mode correlation assumption
E-mode trusts that asset pairs remain correlated. stETH-ETH depeg in 2022
showed this assumption can break. Under e-mode, LTVs go up to 93% — tiny
margin. When correlation breaks, cascade is fast and simultaneous.

### Bank run dynamics
Unlike a bank, lending protocol has no fractional reserve — but at 100%
utilization, suppliers cannot withdraw. This is structurally a run vector:
if suppliers believe others will run, rational strategy is to run first.
