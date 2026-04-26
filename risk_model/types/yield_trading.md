---
id: yield_trading
name: Yield Trading Protocol
description: Splits yield-bearing assets into fixed-rate (PT) and yield (YT) components.
examples: [pendle, element_finance, sense_protocol]
key_risks:
  - deep_chain_yield_trading
  - underlying_protocol_pause
  - concentrated_pool_dependency
  - lp_pullout
  - oracle_coverage_absence
  - maturity_cliff_exploit
  - liquidity_at_maturity
key_parameters:
  - maturity_date
  - implied_apy_at_issuance
  - lp_fee_tier
  - pt_oracle_config
  - yt_pricing_method
key_invariants:
  - "PT + YT = 1 underlying asset  (always)"
  - "PT value approaches face_value (1 underlying) as maturity approaches"
  - "YT value approaches 0 as maturity approaches  (all yield extracted)"
  - "implied_apy = f(PT_price, time_to_maturity)"
attack_patterns:
  - maturity_cliff_exploit
---

## Mechanism

Deposit yield-bearing asset (e.g., stETH) → receive:
- PT (Principal Token): redeemable for 1 stETH at maturity
- YT (Yield Token): claims all yield generated between now and maturity

PT trades at discount to underlying (reflects time value).
YT trades based on expected future yield (highly speculative).

## Type-specific risk profile

### PT and YT are composability primitives
PT and YT are increasingly used as collateral in lending protocols.
Risk profile of PT as collateral: maturity cliff (value jumps to face value
at maturity → predictable jump = arb target), plus dependency on underlying
yield source performing as expected.

### YT = leveraged yield bet
YT holder pays upfront for claim on future yield. If underlying yield
collapses (e.g., staking rewards cut), YT approaches zero.
High volatility + low liquidity = substantial slippage on exit.

### Maturity creates predictable price discontinuity
At maturity, PT snaps to exactly 1 underlying. If PT was trading at discount,
holders profit. This creates:
- Predictable front-running target near maturity
- Cascading liquidations if PT used as collateral in lending and large positions
  held by over-leveraged borrowers near maturity date

### Liquidity cliff at maturity
After maturity, PT and YT markets are redundant. Liquidity migrates to new
maturity. Gap window: old pool is illiquid, new pool has no depth.
Lending protocols accepting PT as collateral face oracle illiquidity during this gap.

### Underlying yield source dependency
PT/YT of rsETH = exposure to rsETH yield = EigenLayer AVS rewards.
If AVS rewards collapse → implied APY collapses → PT reprices → YT worthless.
Full 4-layer dependency stack inherited.
