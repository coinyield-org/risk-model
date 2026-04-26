---
id: lst
name: Liquid Staking Token
description: Token representing staked ETH (or other PoS asset) with on-chain redemption.
examples: [lido_steth, rocketpool_reth, coinbase_cbeth, frax_sfrxeth, mantle_meth]
key_risks:
  - validator_avs_slashing
  - withdrawal_queue_delay
  - exchange_rate_vs_market_depeg
  - validator_operator_risk
  - oracle_coverage_absence
  - underlying_protocol_pause
  - rebasing_semantics
  - concentrated_pool_dependency
  - issuer_blacklist_function
key_parameters:
  - exchange_rate_update_frequency
  - validator_operator_count
  - slashing_insurance_coverage
  - withdrawal_queue_target_wait
  - node_operator_selection_criteria
key_invariants:
  - "exchange_rate = total_staked_eth / total_lst_supply  (increases over time)"
  - "market_price ≈ exchange_rate  (arbitrageable via withdrawal)"
  - "withdrawal_queue_depth / daily_validator_exits <= max_wait_days"
attack_patterns:
  - withdrawal_queue_blocking_lst
  - emode_correlation_engineering
---

## Mechanism

User deposits ETH → protocol stakes with validators → issues LST representing
claim on staked ETH + accrued rewards. Exchange rate grows as staking rewards
accumulate. Redemption: burn LST → enter withdrawal queue → receive ETH
(Ethereum validator exit rate: ~1800 validators/day).

## Type-specific risk profile

### Market price vs exchange rate duality
LST has TWO valid prices:
1. Exchange rate (fundamental: ETH per LST based on staking rewards)
2. Market price (secondary market, driven by demand/supply)

Under normal conditions they converge via arb (if price < exchange rate,
buy LST, queue withdrawal, profit). Under stress (long queue), arb is
blocked and prices diverge. Lending protocols that use ONLY exchange rate
oracle are exposed to market-price depeg.

### Validator slashing: visible and invisible
Visible slashing: on-chain slash event, immediate LST exchange rate drop.
Invisible slashing risk: systemic bug in Ethereum consensus client could
cause mass slashing affecting all validators using that client.
Lido ~75% of validators run Prysm/Lighthouse → client concentration risk.

### Withdrawal queue dynamics
Ethereum caps validator exits at ~57,600 ETH/day under normal conditions.
Full queue (if large LST holder initiates mass withdrawal) delays arbitrage
by days to weeks. This is a known attack vector (see withdrawal_queue_blocking).

### Operator concentration (Lido)
Lido node operator set (~30 professional operators) creates concentration risk.
Single large operator slashing = significant exchange rate drop.
