---
id: stableswap
name: Stableswap AMM
description: AMM optimized for pegged asset pairs; amplified concentration around peg.
parent_type: dex_amm
examples: [curve_3pool, curve_tricrypto, balancer_stable_pools, platypus]
key_risks:
  - readonly_reentrancy
  - thin_liquidity_source_manipulation
  - emode_correlation_break
  - concentrated_pool_dependency
  - stablecoin_depeg
  - amplification_misconfig
  - lp_pullout
key_parameters:
  - amplification_factor_A
  - fee_params
  - admin_fee
  - oracle_ema_params
key_invariants:
  - "StableSwap: A*n^n*sum(x_i) + D = A*D*n^n + D^(n+1)/(n^n * prod(x_i))"
  - "All assets assumed to be at peg; A amplifies liquidity concentration near peg"
  - "When peg breaks: A works against LPs (concentrated in wrong range)"
attack_patterns:
  - forced_selling_cascade_collateral
---

## Mechanism

StableSwap (Curve) invariant concentrates liquidity near peg.
Amplification factor A:
- High A = deep liquidity at peg, terrible slippage far from peg
- Low A = smoother curve (behaves like xy=k)

## Type-specific risk profile

### Amplification factor is a double-edged sword
When all pool assets are at peg → excellent capital efficiency, low slippage.
When one asset depegs → pool becomes single-sided rapidly, IL is severe.
USDC depeg in March 2023: 3pool became USDT+DAI-heavy, USDC drained at near-peg.
LPs couldn't exit until pool rebalanced.

### Admin can change A mid-pool
Curve pools allow governance to ramp A up or down over time. An aggressive
A-increase moves liquidity to center; if depeg happens during ramp → asymmetric
exposure. Small window for front-running A changes.

### Read-only reentrancy (Curve-specific)
Curve's remove_liquidity updates balances after burning LP tokens. Between
these two operations, a contract can re-enter and read stale virtual_price.
This was exploited in July 2023 against Vyper-compiled pools.

### Pool as systemic oracle
Curve 3pool is canonical USD oracle for many protocols.
3pool composition shift (USDC depeg) = corrupted oracle for downstream.
