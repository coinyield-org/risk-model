---
id: synthetic
name: Synthetic Asset Protocol
description: Mints tokenized exposure to any asset via debt pool or collateral-backed mechanism.
examples: [synthetix_v3, lyra, kwenta, gmx_synthetic_perps, mirror_protocol]
key_risks:
  - thin_liquidity_source_manipulation
  - oracle_staleness
  - quoted_vs_underlying_depeg
  - debt_pool_skew
  - overcollateral_ratio_erosion
  - governance_hostile_decision
  - perp_funding_feedback
  - incentive_end_liquidity_flight
key_parameters:
  - global_collateral_ratio
  - min_collateral_ratio
  - skew_scale
  - oracle_source
  - debt_pool_composition
  - liquidation_ratio
key_invariants:
  - "global_debt = sum(synth_supply_i * price_i)  for all synths"
  - "total_collateral_value >= global_debt * min_ratio"
  - "staker_pnl = staker_share * (collateral_change - global_debt_change)"
  - "minter_debt_share proportional to minted_value / global_debt_at_mint_time"
attack_patterns:
  - deleveraging_telegraph_frontrun
  - perp_basis_death_spiral
---

## Mechanism (Synthetix-style debt pool)

SNX stakers collateralize system → collectively back all synth debt.
User mints sUSD → borrows against SNX. All stakers share global debt.
If market moves: stakers who minted sUSD while global_debt was X
now owe their_share * current_global_debt.
Oracle provides all synth prices → staker exposure = short on all synths.

## Type-specific risk profile

### Global debt pool = shared risk

Staker mints 1000 sUSD when global debt = 10,000 USD → 10% debt share.
Other synths (sBTC, sETH) appreciate → global_debt = 20,000 USD.
Staker now owes 2000 USD but still has 1000 sUSD → personal loss.

This means: even if a staker mints only sUSD, they're short all other synths.
This is a non-obvious composability risk.

### Oracle loop in debt pool
Synth price comes from oracle. Oracle price × outstanding synth supply = global debt.
Global debt → liquidation thresholds for all stakers. If oracle manipulated
on any synthetic → distorted global debt → wrong liquidations across system.

Worse: if synth price inflated, all sETH holders profit at expense of stakers.
Stakers are involuntary counterparty to oracle manipulation.

### Skew as attack surface
Synthetix V3 uses skew-based funding to incentivize balance. When skew is
extreme (all synthetic longs, no shorts), protocol has direct P&L exposure.
Large attacker can push skew, then move underlying price (or manipulate oracle).

### Debt share dilution
New minters dilute existing debt shares. During high periods of new minting
(e.g., yield farming incentives), existing stakers find their debt share
recalculated at each block. Front-running high-debt periods = arb opportunity.
