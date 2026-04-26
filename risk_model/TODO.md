# Risk Model TODO

This file tracks implementation work for the DeFi risk graph.

`ARCHITECTURE.md` explains the model. This file tracks what remains to build.

## Current Limitations

- Protocol files are still Markdown frontmatter, not pure canonical YAML.
- Market and pool nodes are not first-class yet.
- Asset nodes are currently inferred from dependency fields, not curated files.
- External dependencies are inferred from protocol dependencies.
- Unknown `risk_id` references are currently cleaned up, but strict CI/import
  failure is not enforced yet.
- Edge properties do not yet include real exposure metrics for most relationships.
- `propagation_coeff`, `confidence`, and `observed_at` are mostly not populated.
- Recursive dependencies are visible only where protocol files already mention them.

## Recommended Direction

Keep current protocol Markdown files for now. They are useful risk cards and
reviewable documentation.

For new graph precision, add new structured YAML files first:

```text
assets/
markets/
pools/
entities/
edges/
```

Later, if the model becomes more automated, split protocol files into:

```text
nodes/protocols/curve.yaml      canonical machine-readable data
docs/protocols/curve.md         human-readable rationale
```

Do not rush this split. The immediate priority is to add the missing exposure
layers and make cascade questions answerable.

## Tasks

### 1. Keep Risk IDs Clean

Current status: the importer runs with zero unknown `risk_id` warnings.

- Add alias handling for renamed IDs.
- Fail CI/import when a new unknown risk ID appears.
- Keep category IDs out of `active_risks` and `key_risks`; use concrete risk IDs.

### 2. Model Upgradeable Proxy and Admin Key Risks

Do not add separate proxy, multisig, or signer nodes yet.

For now, model these risks directly on protocol or deployment nodes:

```yaml
active_risks:
  - risk_id: proxy_upgrade_authority
    deployment: ethereum
    note: "Contracts are upgradeable through proxy admin."

  - risk_id: governance_signer_key_leak
    deployment: ethereum
    note: "Compromise of enough proxy-admin/governance signers can authorize a malicious implementation upgrade."
```

Use the distinction consistently:

- `proxy_upgrade_authority` = the protocol has legitimate upgrade authority.
- `deployer_key_leak` = deployer or upgrade EOA private key compromise.
- `governance_signer_key_leak` = multisig/governance signer compromise.
- `guardian_key_leak` = emergency/guardian key compromise.

Avoid the non-canonical umbrella `admin_key_compromise` unless it is added to
taxonomy as an alias or canonical risk.

### 3. Add Asset Files

Add curated asset nodes:

```text
risk_model/assets/usdc.yaml
risk_model/assets/wsteth.yaml
risk_model/assets/rseth.yaml
risk_model/assets/wbtc.yaml
```

Each asset should include:

```yaml
id: asset:wsteth
symbol: wstETH
type: lst
issuer_protocol: lido
underlying: ETH
native_chain: ethereum
active_risks:
  - withdrawal_queue_delay
  - exchange_rate_vs_market_depeg
```

### 4. Add Market / Pool Files

Add concrete exposure units:

```text
risk_model/markets/aave_v3.ethereum.wsteth.yaml
risk_model/pools/curve.ethereum.steth_eth.yaml
risk_model/vaults/morpho.ethereum.steakhouse_usdc.yaml
```

Each market/pool should include:

```yaml
id: market:aave_v3.ethereum.wsteth
protocol: aave_v3
chain: ethereum
collateral_asset: wstETH
oracle: chainlink_wsteth_eth
ltv: 0.80
liquidation_threshold: 0.82
supply_cap: 1200000
tvl_usd: 4200000000
```

### 5. Add Edge Schema Validation

Define strict JSON Schema or YAML schema for:

```text
protocol
deployment
asset
market
pool
entity
edge
risk
```

The importer should eventually reject invalid files instead of tolerating all
YAML-like prose.

### 6. Add Exposure-Based Propagation

Populate:

```text
exposure_usd
exposure_pct_of_protocol_tvl
ltv
liquidation_threshold
liquidity_depth_usd
propagation_coeff
confidence
observed_at
```

This turns the graph from "connected/not connected" into a ranked risk model.

### 7. Add Reports

Generate reports from Neo4j:

```text
shared_dependency_report.md
blast_radius_lido.md
blast_radius_circle.md
recursive_assets.md
missing_taxonomy_ids.md
top_cascade_paths.md
```

### 8. Add Incident / Event Evidence Layer

Add structured incident files so each `risk_id` can answer:

```text
show the latest 5 incidents related to this risk
```

Use a new directory:

```text
risk_model/incidents/
```

Each incident should include:

```yaml
id: incident:hyperliquid_jelly_2024
title: "Hyperliquid JELLY incident"
date: 2024-03-01
event_type: bad_debt | exploit | depeg | oracle_failure | governance | bridge | liquidation
amount_lost_usd: 0
affected_protocols: [hyperliquid_hlp]
affected_assets: [JELLY]
chains: [hyperliquid_l1]
risk_ids:
  - bad_debt_socialization
  - whale_concentration
source_urls:
  - https://example.com
confidence: high
notes: "Short explanation of why this incident evidences the listed risks."
```

Graph model:

```text
(:Incident)-[:EVIDENCES_RISK]->(:Risk)
(:Incident)-[:INVOLVES_PROTOCOL]->(:Protocol)
(:Incident)-[:INVOLVES_ASSET]->(:Asset)
(:Incident)-[:INVOLVES_CHAIN]->(:Chain)
```

Initial query:

```cypher
MATCH (:Risk {risk_id: $risk_id})<-[:EVIDENCES_RISK]-(i:Incident)
RETURN i.date, i.title, i.amount_lost_usd, i.source_urls
ORDER BY i.date DESC
LIMIT 5;
```

Later, incidents can also attach to specific market/exposure edges once those
edges become first-class nodes.

### 9. Add Feedback Loop Detection

Search for cycles:

```text
lending collateral
  -> liquidation sell pressure
  -> DEX pool price
  -> oracle/TWAP
  -> lending health factor
```

This is especially important for Curve, Uniswap, Aave, Morpho, Pendle, and LST/LRT
markets.

### 10. Add Bad Debt and Reflexive Bank-Run Scenario Model

Model cases where an upstream exploit creates bad debt in a lending protocol and
then triggers depositor withdrawals / TVL flight.

Example scenario:

```text
KelpDAO exploit
  -> rsETH depeg / backing impairment
  -> attacker borrows ETH on Aave against mispriced rsETH
  -> Aave bad debt
  -> suppliers withdraw because losses may be socialized
  -> utilization spikes
  -> TVL drops and remaining users face worse liquidity
```

Do not treat this as a simple `exposure_usd * propagation_coeff` case. Split it
into three layers:

```text
1. Direct bad debt
2. Solvency / absorption shock
3. Reflexive bank-run / confidence shock
```

Fields needed at market level:

```yaml
market:
  supplied_usd: 0
  borrowed_usd: 0
  utilization: 0.0
  available_liquidity_usd: 0
  borrow_cap_remaining_usd: 0
  collateral_factor: 0.0
  liquidation_threshold: 0.0
  liquidation_depth_usd: 0
  oracle_model: market_price | exchange_rate | stale_possible
```

Fields needed at protocol level:

```yaml
protocol:
  tvl_usd: 0
  reserves_usd: 0
  safety_module_usd: 0
  bad_debt_absorption_mechanism: reserve | safety_module | suppliers | governance | unknown
  withdrawal_liquidity_by_asset: {}
```

Fields needed at scenario level:

```yaml
scenario:
  upstream_loss_usd: 0
  depeg_pct: 0.0
  oracle_lag_minutes: 0
  attacker_collateral_usd: 0
  confidence_shock: low | medium | high
```

Initial calculation structure:

```text
max_borrow = oracle_collateral_value * ltv
true_collateral_value = oracle_collateral_value * (1 - depeg_pct)
liquidation_recovery = true_collateral_value * recovery_rate
bad_debt = max(0, max_borrow - liquidation_recovery)
```

Then estimate run pressure from ratios:

```text
bad_debt / protocol_tvl
bad_debt / market_supplied_usd
bad_debt / reserves_usd
bad_debt / safety_module_usd
available_liquidity_usd / supplied_usd
```

Output should distinguish:

```text
mechanical_loss_usd
expected_bad_debt_usd
absorption_capacity_usd
residual_loss_usd
estimated_tvl_flight_pct
confidence: low | medium | high
```

### 11. Productionize Neo4j Runtime

Current local runtime is Docker Compose for development and graph exploration.
Before production, add:

- Managed Neo4j or production-grade self-hosted deployment plan.
- Secrets management for `NEO4J_AUTH`, user, password, and Bolt URI.
- Backup and restore procedure.
- Import strategy:
  - dev: clear + full import is acceptable;
  - prod: versioned import / migrations / idempotent updates with stale-node cleanup.
- CI checks:
  - importer runs with zero unknown `risk_id`;
  - generated Cypher is up to date;
  - schema validation passes;
  - sample Cypher queries return expected node counts.
- Monitoring:
  - DB health;
  - import duration;
  - query latency;
  - disk usage;
  - failed auth/import attempts.
- Query API layer for application usage:
  - blast radius;
  - shared dependencies;
  - active risks;
  - scenario paths;
  - exposure-weighted cascade ranking.
