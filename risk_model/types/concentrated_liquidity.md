---
id: concentrated_liquidity
name: Concentrated Liquidity AMM
description: AMM where LP provides liquidity within custom price ranges (tick-based).
parent_type: dex_amm
examples: [uniswap_v3, uniswap_v4, ambient, pancakeswap_v3, camelot_v3]
key_risks:
  - lp_position_single_sided_trap
  - thin_liquidity_source_manipulation
  - oracle_coverage_absence
  - lp_pullout
  - concentrated_pool_dependency
  - flash_loanability
  - governance_hostile_decision
key_parameters:
  - fee_tier
  - tick_spacing
  - active_range_depth
  - oracle_observation_window
key_invariants:
  - "Liquidity active only within [tickLower, tickUpper]"
  - "Outside range: position is 100% in one asset (impermanent loss realized)"
  - "Virtual reserves: L/sqrt(P) = virtual_x, L*sqrt(P) = virtual_y"
  - "Price = tick where current liquidity is concentrated"
attack_patterns:
  - lp_position_single_sided_trap
  - gas_ddos_liquidation
---

## Mechanism

LPs choose price range [lower, upper]. Within range: standard AMM with concentrated
virtual liquidity. Outside range: LP holds 100% of one asset, earns no fees.
Capital efficiency vs range management tradeoff.

## Type-specific risk profile

### LP NFT as collateral — single-sided trap
Uniswap V3 LP positions are NFTs increasingly used as collateral.
Attacker can move price outside LP range → position becomes 100% single-asset.
Collateral value drops not from price drop but from range-out mechanics.
Lending protocols accepting V3 NFTs need real-time range-state oracle.

### Just-in-time liquidity (JIT)
Large trades can be front-run by an LP depositing into exact tick just before
the trade and withdrawing just after. This extracts fees from regular LPs and
results in worse price discovery.

### Tick boundary manipulation
When price crosses a tick boundary, large amount of liquidity may enter/exit
instantly. Flash loans can engineer price to land at specific tick, manipulating
virtual_price at that boundary.

### TWAP manipulation window
Uniswap V3 TWAP oracle accumulates time-weighted tick observations. Thin
liquidity at specific tick = easy price movement = TWAP manipulation over
observation window.
