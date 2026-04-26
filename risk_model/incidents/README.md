# Incidents

This directory contains structured incident records that link real-world DeFi events to
risk taxonomy IDs. Each file represents one incident and is used to validate and calibrate
the risk model.

## File naming

```
{YYYY-MM-DD}_{short_slug}.yaml        # hand-authored
auto_{YYYY-MM-DD}_{short_slug}.yaml   # auto-generated, needs human review
```

## Schema

Every incident YAML must conform to the following schema:

```yaml
id: incident:YYYY-MM-DD_short_slug         # e.g. incident:2023-03-10_usdc_svb_depeg
title: "Human-readable title"
date: YYYY-MM-DD
event_type: bad_debt | exploit | depeg | oracle_failure | governance | bridge | liquidation | cascade
amount_lost_usd: 0                         # 0 if near-miss or recovered
near_miss: false                           # true if funds recovered or harm avoided
affected_protocols: []                     # slugs from risk_model/protocols/
affected_assets: []                        # ticker symbols
chains: []                                 # chain IDs from risk_model/chains/
root_cause_entity: ""                      # optional: which protocol/entity triggered it
cascade_targets: []                        # for cascade events: downstream protocols affected
risk_ids:                                  # required: links to taxonomy risk IDs
  - risk_id_from_taxonomy
source_urls: []
confidence: low | medium | high
notes: "Why this incident evidences the listed risk_ids."
```

## Field reference

### `id`
Globally unique string. Format: `incident:YYYY-MM-DD_short_slug`. The slug should be
lowercase, words separated by underscores, descriptive enough to identify the event at a
glance. Example: `incident:2023-11-10_heco_bridge_hack`.

### `title`
Free-form human-readable title. Aim for under 80 characters.

### `date`
ISO 8601 date (`YYYY-MM-DD`) of when the incident occurred (not when it was discovered or
reported).

### `event_type`
One of the following enumerated values:

| Value | Meaning |
|-------|---------|
| `bad_debt` | Protocol accrued bad debt that was not fully covered |
| `exploit` | Smart-contract or protocol-level exploit |
| `depeg` | Asset lost its peg (stablecoin, LST, bridged token, etc.) |
| `oracle_failure` | Incorrect or manipulated price feed triggered losses |
| `governance` | Malicious or erroneous governance action |
| `bridge` | Bridge hack, theft, or asset-backing loss |
| `liquidation` | Cascade liquidation or broken liquidation mechanics |
| `cascade` | Multi-protocol contagion event |

### `amount_lost_usd`
Estimated USD value of funds lost at time of incident. Use `0` for near-misses or events
where all funds were ultimately recovered.

### `near_miss`
`true` if no funds were permanently lost (e.g., exploit was caught pre-execution, or funds
were fully recovered via negotiation or white-hat return).

### `affected_protocols`
List of protocol slugs from `risk_model/protocols/`. Use only slugs that exist in that
directory. Leave empty if no known protocol slug matches.

Known slugs:
`aave_v3`, `arbitrum_bridge`, `aster_bridge`, `babylon`, `base_bridge`, `bedrock`,
`binance_btc`, `bouncebit`, `buzz_farming`, `cap`, `coinbase_bridge`, `coinbase_cbeth`,
`compound_v3`, `convex`, `curve`, `eigenlayer`, `ethena`, `etherfi`, `etherfi_liquid`,
`frax`, `free_protocol`, `grove_finance`, `hyperlend`, `hyperliquid`, `hyperliquid_hlp`,
`jupiter_lend`, `jupiter_perps`, `jupiter_staked_sol`, `justlend`, `kamino`, `kelp`,
`kraken_bitcoin`, `lido`, `lombard_lbtc`, `m0`, `maple`, `mellow`, `meth_protocol`,
`morpho`, `ondo`, `optimism_bridge`, `pancakeswap`, `pendle`, `polygon_bridge`,
`portal_wormhole`, `renzo`, `rocket_pool`, `sky_lending`, `solv_btc`, `spark_liquidity`,
`sparklend`, `ssv_network`, `stacks_sbtc`, `stader`, `steakhouse`, `symbiotic`, `tbtc`,
`tornado_cash`, `unirouter`, `uniswap_v3`, `uniswap_v4`, `upshift`, `venus`, `wbeth`,
`wbtc`, `yearn`

### `affected_assets`
List of ticker symbols for assets directly involved (e.g., `["USDC", "WETH"]`).

### `chains`
List of chain IDs from `risk_model/chains/`.

Known chain IDs:
`arbitrum`, `avalanche`, `base`, `bitcoin`, `bnb`, `centrifuge`, `ethereum`, `gnosis`,
`hyperliquid_l1`, `linea`, `mantle`, `merlin_chain`, `optimism`, `polygon`, `provenance`,
`solana`, `tron`

### `root_cause_entity`
Optional free-form string identifying which protocol, team, or external entity was the
primary root cause (when different from `affected_protocols`).

### `cascade_targets`
For `event_type: cascade` events, list the downstream protocol slugs that were impacted as
a result of the root event.

### `risk_ids`
**Required.** One or more risk IDs from the taxonomy that this incident evidences. At least
one must be provided. Valid values by category:

**oracle**
`thin_liquidity_source_manipulation`, `oracle_staleness`, `deviation_threshold_too_wide`,
`quoted_vs_underlying_depeg`, `sequencer_uptime_feed_missing`, `readonly_reentrancy`,
`fallback_oracle_misconfig`, `feed_deprecation_by_provider`, `aggregator_upgrade_by_provider`,
`quote_currency_mismatch`, `circuit_breaker_false_trigger`, `twap_window_misconfig`

**admin_governance**
`governance_hostile_decision`, `guardian_asymmetric_authority`, `risk_stewards_narrow_window`,
`l2_executor_divergence`, `proxy_upgrade_authority`, `timelock_mismatch`,
`emergency_action_conflict`

**key_compromise**
`governance_signer_key_leak`, `guardian_key_leak`, `oracle_operator_key_leak`,
`keeper_bot_key_leak`, `validator_key_share_compromise`, `sequencer_operator_key_leak`,
`deployer_key_leak`

**governance_attack**
`hostile_proposal_via_delegation`, `flash_governance`, `vote_buying`, `proposal_griefing`,
`low_turnout_capture`, `delegate_single_point_failure`

**collateral_asset**
`stablecoin_depeg`, `lst_lrt_depeg`, `bridged_backing_loss`, `issuer_blacklist_function`,
`issuer_pause_function`, `rebasing_semantic_confusion`, `underlying_protocol_pause`,
`validator_avs_slashing`, `rwa_issuer_default`

**liquidation_mechanics**
`liquidation_bonus_too_small`, `liquidation_bonus_too_large`, `close_factor_limits`,
`dust_positions_uneconomic`, `single_keeper_dependency`, `liquidation_sandwich`,
`gas_wars_revert`, `block_gas_limit_mass_liquidation`, `gas_ddos_liquidation`,
`illiquid_collateral_liquidation`, `l2_fee_spike_unprofitable`, `mempool_censorship`

**market_liquidity**
`utilization_full_bank_run`, `bad_debt_socialization`, `bad_debt_accumulation`,
`insurance_fund_depletion`, `tvl_concentration_single_strategy`, `debt_pool_skew`,
`lp_position_single_sided_trap`, `ir_curve_kink_miscalibration`, `safety_module_slash_exposure`,
`incentive_end_liquidity_flight`, `supply_borrow_cap_mismatch`, `native_stablecoin_peg_stress`

**external_dependencies**
`oracle_provider_dep`, `l2_sequencer_dep`, `bridge_dep`, `staking_protocol_dep`,
`restaking_protocol_dep`, `underlying_chain_dep`, `rpc_infra_dep`, `builder_relay_dep`,
`operator_concentration`, `bridge_signing_committee`

**temporal_reflexivity**
`withdrawal_queue_delay`, `systemic_reflexivity`, `self_fulfilling_depeg`,
`perp_funding_feedback`, `harvest_sandwich`, `maturity_cliff_exploit`,
`liquidity_at_maturity`, `governance_timelock_vs_attack_speed`

**social_coordination**
`contagion_bank_run`, `whale_concentration`, `fud_campaign`, `insider_asymmetry`

**infrastructure**
`chain_reorg`, `chain_halt`, `l2_finality_delay`, `rpc_outage`, `sequencer_downtime`,
`sequencer_centralization`

**cross_chain**
`bridge_pause_censorship`, `message_replay_ordering`, `canonical_vs_bridged_coexistence`,
`per_deployment_divergence`, `timelock_skew_cross_chain`

**offchain_social_tech**
`frontend_dns_hijack`, `frontend_ipfs_gateway`, `frontend_js_injection`,
`wallet_supply_chain`, `governance_forum_manipulation`, `delegate_social_engineering`

**token risks**
`minter_authority`, `blacklist_function`, `pause_function`, `upgrade_authority`,
`minter_key_leak`, `freeze_admin_key_leak`, `custodian_signer_leak`,
`offchain_custodian_risk`, `reserve_concentration`, `rwa_counterparty_default`,
`undercollateralization_via_bad_debt`, `bridge_lock_backing_loss`,
`validator_slashing_erosion`, `avs_slashing_erosion`, `hard_peg_redemption_window_closed`,
`soft_peg_algo_failure`, `exchange_rate_vs_market_depeg`, `wrapped_custodian_risk`,
`death_spiral`, `depeg_feedback_loop`, `unauthorized_mint`, `concentrated_pool_dependency`,
`incentive_mercenary_tvl`

### `source_urls`
List of URLs to primary sources (post-mortems, Rekt News, Twitter threads, governance
forum posts). Aim for at least one authoritative source per incident.

### `confidence`
How confident the author is that the `risk_ids` mapping is correct:

| Value | Meaning |
|-------|---------|
| `low` | Auto-generated or based on secondary sources; needs human review |
| `medium` | Based on a credible post-mortem or primary source, mapping is plausible |
| `high` | Mapping reviewed by a domain expert against the full post-mortem |

### `notes`
Free-form explanation of why this incident evidences the listed `risk_ids`. Should be
specific enough that a reviewer can verify the mapping without reading the source URLs.

## Authoring guidelines

1. Each file covers exactly one incident. If a single event affected multiple protocols
   simultaneously, use `cascade_targets` rather than creating separate files.
2. Auto-generated files (`auto_*.yaml`) have `confidence: low` and must be reviewed before
   being treated as authoritative. Promote confidence only after checking against a primary
   post-mortem.
3. `risk_ids` must contain only values from the taxonomy above. If no taxonomy ID fits,
   add a comment explaining why and leave `risk_ids` empty — do not invent new IDs.
4. `amount_lost_usd` should be the commonly cited figure at time of incident in USD.
   Do not retroactively adjust for token price changes.
5. When uncertain about `affected_protocols`, leave the list empty rather than guessing.

## Bootstrap scripts

Two generators feed `auto_*.yaml` stubs into this directory:

### `bootstrap_defillama.py` — DeFiHackLabs READMEs

Parses the SunWeb3Sec/DeFiHackLabs GitHub READMEs (2020–present) and generates
stubs for events whose attack-type text maps to an in-scope taxonomy risk.
Out-of-scope code bugs (reentrancy, precision loss, ACL bugs, etc.) are
skipped.

```bash
python risk_model/incidents/bootstrap_defillama.py
python risk_model/incidents/bootstrap_defillama.py --out-dir /path/to/incidents
```

### `bootstrap_hacks_txt.py` — DefiLlama hacks.txt list

Parses a plain-text dump of the DefiLlama hacks feed in
`N. Name | Date | Amount | URL` format. Centralised exchange, wallet, and
social-media-only incidents are excluded. Well-known incidents (Ronin, Mango,
Multichain, Beanstalk, Tornado Cash, UwU Lend, etc.) are promoted to
`medium`/`high` confidence via the `KNOWN_INCIDENTS` override table. Entries
not matched by a keyword rule are written with empty `risk_ids` and a note
requesting manual review.

```bash
python risk_model/incidents/bootstrap_hacks_txt.py
python risk_model/incidents/bootstrap_hacks_txt.py --input path/to/hacks.txt --dry-run
```

Review every generated file and raise `confidence` from `low` to `medium` or
`high` after verifying the mapping against a primary source.
