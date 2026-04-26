---
id: yield_aggregator
name: Yield Aggregator
description: Automates capital deployment across yield strategies; compounds returns.
examples: [yearn_v3, beefy, harvest_finance, convex, aura, sommelier]
key_risks:
  - underlying_protocol_pause
  - downstream_protocol_failure
  - harvest_sandwich
  - single_keeper_dependency
  - governance_hostile_decision
  - proxy_upgrade_authority
  - incentive_end_liquidity_flight
  - tvl_concentration_single_strategy
key_parameters:
  - withdrawal_fee
  - performance_fee
  - strategy_allocation
  - harvest_trigger_threshold
  - max_loss_tolerance
key_invariants:
  - "share_price = total_assets / total_shares"
  - "share_price monotonically non-decreasing  (else negative yield)"
  - "withdrawal_amount >= deposit_amount * (1 - max_loss)"
attack_patterns:
  - harvest_sandwich
  - retroactive_airdrop_tvl_farming
---

## Mechanism

Vault aggregates user deposits → deploys into one or more yield strategies.
Keeper triggers harvest() → claims rewards → compounds back into position.
Share price = total_assets / total_shares; increases as yield accrues.

## Type-specific risk profile

### Strategy = sum of underlying protocol risks
Aggregator inherits ALL risks of every strategy it uses. Yearn strategy
deploying into Aave + Curve + Convex = Aave risks + Curve risks + Convex risks.
A single strategy failure can drain the vault.

### Harvest sandwich
harvest() function is public and often gas-compensated. Before harvest:
underlying assets have accrued yield not yet reflected in share price.
Attacker: flash-deposits → triggers harvest (price jumps) → withdraws.
Extracts yield accrued by other depositors.
Mitigation: deposit/harvest delay, anti-front-running fee.

### TVL concentration
When vault has $500M in single strategy (Convex-style), vault IS the market.
Rebalancing creates price impact on itself. Strategy changes become public
signals for arbitrageurs.

### Strategy migration risk
When vault migrates from strategy A to B: during migration, assets may sit
idle (no yield) or in transition state. Withdrawal during migration may hit
edge cases in accounting.

### Keeper single point of failure
If no keeper triggers harvest, yield doesn't compound. Some vaults have
permissionless harvest (anyone can call) — but gas economics may make it
unprofitable for small vaults.
