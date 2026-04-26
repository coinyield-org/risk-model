---
id: dex_amm
name: DEX AMM (Constant Product)
description: Automated market maker with xy=k invariant or variants; passive LP model.
examples: [uniswap_v2, sushiswap, pancakeswap, camelot_v2]
subtypes: [stableswap, concentrated_liquidity]
key_risks:
  - thin_liquidity_source_manipulation
  - readonly_reentrancy
  - incentive_end_liquidity_flight
  - concentrated_pool_dependency
  - lp_pullout
  - oracle_coverage_absence
  - whale_concentration
  - governance_hostile_decision
key_parameters:
  - fee_tier
  - lp_token_pricing_method
  - oracle_window_if_used_as_twap_source
key_invariants:
  - "reserve_x * reserve_y = k  (constant product)"
  - "spot_price = reserve_y / reserve_x"
  - "LP_share_value = 2 * sqrt(reserve_x * reserve_y) / total_supply"
attack_patterns:
  - gas_ddos_liquidation
---

## Mechanism

LPs deposit token pairs in 50/50 ratio → receive LP tokens representing pool share.
Price adjusts automatically as traders buy/sell: price impact = trade_size / pool_depth.
Fees accumulate to LP tokens.

## Type-specific risk profile

### AMM as oracle source
Many protocols use AMM TWAP as price oracle. This makes DEX and downstream protocols
co-dependent: manipulating DEX price (even temporarily) affects downstream lending,
CDP, synthetic protocols.

TWAP window trade-off:
- Too short: manipulable in few blocks
- Too long: lags real price, creates profitable liquidation/borrow windows

### Impermanent loss isn't a risk here
IL is a known LP economics tradeoff, not a systemic risk vector (it's priced in).
What IS a risk: liquidity concentration + sudden LP exit under stress.

### Read-only reentrancy
If AMM updates balances before minting/burning LP tokens (or vice versa), and
downstream reads reserves mid-function, it reads inconsistent state. Curve-style
AMMs were exploited this way. Consumers of AMM reserves as oracle must check
this.

### Mercenary LP dynamics
High-emission pools attract LP that leaves immediately when rewards end.
Sudden depth collapse = wider spreads = worse oracle = downstream protocol risk.
