---
id: perps
name: Perpetual Futures Protocol
description: Leveraged synthetic long/short positions on assets with funding rate mechanism.
examples: [gmx_v2, dydx_v4, hyperliquid, gains_network, synthetix_perps, kwenta]
key_risks:
  - thin_liquidity_source_manipulation
  - oracle_staleness
  - quoted_vs_underlying_depeg
  - bad_debt_socialization
  - single_keeper_dependency
  - liquidation_bonus_too_small
  - insurance_fund_depletion
  - perp_funding_feedback
  - governance_hostile_decision
  - sequencer_downtime
key_parameters:
  - max_leverage
  - maintenance_margin
  - liquidation_fee
  - funding_rate_params
  - insurance_fund_size
  - open_interest_caps
  - skew_scale
key_invariants:
  - "funding_rate = f(long_OI - short_OI) / skew_scale"
  - "mark_price ≈ index_price  (funding enforces convergence)"
  - "sum(long_PnL) + sum(short_PnL) = 0  (zero-sum within protocol)"
  - "insurance_fund >= 0  (otherwise socialized loss)"
attack_patterns:
  - deleveraging_telegraph_frontrun
  - perp_basis_death_spiral
  - gas_ddos_liquidation
---

## Mechanism

Users open long/short positions with leverage. Collateral posted as margin.
Funding rate: longs pay shorts when OI skewed long (and vice versa) → converges
mark price to index. When margin < maintenance_margin → liquidation.
Insurance fund absorbs bad debt from undercollateralized liquidations.

## Type-specific risk profile

### Mark price oracle is existential
All P&L and liquidation calculations use mark price (derived from oracle).
Mark price manipulation = instant profits for all positions on correct side +
cascading wrong-side liquidations. Larger OI = larger attack surface.

### Skew imbalance risk
When OI heavily skewed in one direction, protocol acts as counterparty to
excess. GMX-V1 pattern: LPs (liquidity providers) ARE the counterparty.
If majority of traders go long on manipulated price, LPs bear the loss.

### Insurance fund runway
Insurance fund depletes over time under sustained bad debt (insufficient
liquidation coverage). Once depleted → socialized loss → LP/staker flight →
less liquidity → more bad debt → spiral.

### Funding rate reflexivity
Extreme funding rate (positive or negative) creates self-fulfilling dynamics:
high positive funding → shorters enter → funding drops → longers squeezed.
This creates volatility at inflection points.

### L2 sequencer dependency
On L2 perps (most perps are L2), sequencer downtime = positions can't be
managed while prices move. This is catastrophic for leveraged positions.
