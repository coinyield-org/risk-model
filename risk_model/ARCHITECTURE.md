# Risk Model Architecture

## Purpose

This model describes DeFi operational, economic, dependency, centralization, and
cascade risks.

It is not a smart-contract bug database and not a regulatory risk model. Audit
reports are used as context, but the model does not try to duplicate auditor
findings.

The goal is to answer questions like:

- What breaks if Lido withdrawal queues slow down?
- Which protocols share Chainlink, Circle, LayerZero, or one sequencer as a dependency?
- Which assets create recursive risk because they depend on bridges, restaking,
  custodians, or issuer controls?
- Which pools or markets are exposed to the same upstream asset or protocol?
- What is the blast radius of a specific risk event?

## Core Idea

The model should be graph-first.

That means the important objects are represented as nodes, and the way risk moves
between them is represented as edges.

```text
node = object
edge = relationship / dependency / exposure path
```

Example:

```text
protocol:lido
  -> asset:wsteth
  -> market:aave_v3.ethereum.wsteth
  -> deployment:aave_v3.ethereum
  -> protocol:aave_v3
```

The Markdown files are still useful, but they are not the final analytical model.
They are the human-readable layer. Neo4j is the query layer that makes dependency
paths, shared dependencies, and cascades searchable.

## Current Source Data

The current source data lives under `risk_model/`.

```text
risk_model/
  protocols/          protocol risk cards
  types/              base risk profiles by protocol type
  chains/             chain-level risk profiles
  taxonomy/           stable risk IDs and categories
  risks/              detailed risk notes
  attack_patterns/    multi-step attack patterns
  scoring/            scoring policy
  neo4j/              graph schema, importer, generated Cypher, example queries
```

Protocol files currently use Markdown with YAML frontmatter:

```text
---
slug: aave_v3
types: [lending]
deployments: ...
dependencies: ...
active_risks: ...
---

## Overview
...
```

The frontmatter is machine-readable. The Markdown body explains rationale,
mechanics, deployment divergence, and key parameters for human review.

## Layers

The model should be evaluated by layers.

```text
Chain risk
  -> Protocol risk
    -> Deployment risk
      -> Market / pool risk
        -> Asset risk
          -> External entity risk
```

### Chain

Examples:

```text
chain:ethereum
chain:arbitrum
chain:base
chain:solana
```

Chain risks include sequencer downtime, chain halt, finality, bridge assumptions,
RPC concentration, MEV infrastructure, and censorship.

### Protocol

Examples:

```text
protocol:aave_v3
protocol:lido
protocol:curve
protocol:pendle
```

A protocol file is a top-level risk card. It should describe the protocol's role,
types, deployments, upstream dependencies, active risks, audits, and rationale.

It should not contain every pool or market in full detail. Those should become
separate market/pool nodes.

### Deployment

Examples:

```text
deployment:aave_v3.ethereum
deployment:aave_v3.arbitrum
deployment:curve.base
```

Deployments matter because the same protocol can have different risk profiles on
different chains: different assets, bridges, liquidity depth, sequencers,
governance executors, or parameters.

### Market / Pool

Planned examples:

```text
market:aave_v3.ethereum.wsteth
pool:curve.ethereum.steth_eth
market:pendle.ethereum.eeth_pt
vault:morpho.ethereum.steakhouse_usdc
```

This is the most important missing layer today.

Markets and pools are where exposure becomes concrete: TVL, collateral asset,
loan asset, LTV, liquidation threshold, oracle source, pool assets, pool
imbalance, and downstream users.

### Asset

Examples:

```text
asset:usdc
asset:wsteth
asset:rseth
asset:usdc_e
asset:crvusd
```

Asset risk includes issuer control, backing, redemption path, bridge backing,
depeg, blacklist/freeze functions, custody, restaking slashing, and liquidity.

### External Entity

Examples:

```text
entity:chainlink
entity:circle
entity:bitgo
entity:layerzero
entity:coinbase_sequencer
```

These are dependencies that are not always protocols themselves: oracle providers,
issuers, custodians, sequencers, risk curators, bridge committees, operators, or
attestation firms.

## Neo4j Layer

The Neo4j layer is under `risk_model/neo4j/`.

```text
neo4j/
  schema.md
  constraints.cypher
  queries.cypher
  import_risk_model.py
  generated/risk_model.cypher
```

The importer reads current source files and generates Cypher:

```bash
/opt/homebrew/anaconda3/bin/python risk_model/neo4j/import_risk_model.py
```

Current generated graph size:

```text
881 nodes
2354 relationships
```

Neo4j is not the source of truth. It is the query and exploration layer.

## Node Types

Current graph nodes:

```text
Protocol
Deployment
Chain
ProtocolType
Risk
RiskCategory
Asset
PricePair
ExternalDependency
AttackPattern
```

Planned graph nodes:

```text
Market
Pool
Vault
Strategy
OracleFeed
GovernanceBody
Multisig
OperatorSet
```

## Edge Direction

Edges point from the risk consumer to the upstream dependency.

```text
deployment:aave_v3.ethereum -[:DEPENDS_ON]-> protocol:lido
deployment:aave_v3.ethereum -[:DEPENDS_ON]-> dependency:chainlink
deployment:aave_v3.ethereum -[:USES_ASSET]-> asset:wsteth
```

This direction makes dependency questions direct:

```text
What does Aave depend on?
```

Traverse outgoing edges.

Blast-radius questions use the reverse direction:

```text
What is affected if Lido has a problem?
```

Traverse incoming dependency edges.

## Important Edge Properties

Edges should eventually carry more than `id` and `type`.

Important fields:

```yaml
type: accepts_collateral
scope:
  chain: ethereum
  deployment: aave_v3.ethereum
  market: aave_v3.ethereum.wsteth
assets: [wstETH]
exposure:
  tvl_usd: 4200000000
  ltv: 0.80
  liquidation_threshold: 0.82
propagation:
  propagation_coeff: 0.75
confidence: medium
observed_at: 2026-04-21
source: manual
```

The key idea: an edge explains how strongly risk moves from one object to
another.

## Risk Propagation

Severity is two-dimensional:

```text
severity = likelihood x impact
```

A dependency edge can dampen or amplify impact:

```text
effective_impact = upstream_impact * propagation_coeff
```

Example:

```text
Lido withdrawal_queue_delay:
  likelihood = 3
  impact = 4

wstETH -> Aave market edge:
  propagation_coeff = 0.75

effective impact on Aave market:
  4 * 0.75 = 3.0
```

This avoids copying the same risk score everywhere. A risk can be severe at the
source but weaker downstream if the exposure is small, capped, non-collateral, or
well isolated.

## Example: Lido to Aave Cascade

Path:

```text
protocol:lido
  -> asset:wsteth
  -> market:aave_v3.ethereum.wsteth
  -> deployment:aave_v3.ethereum
  -> protocol:aave_v3
```

Event:

```text
Lido withdrawal queue becomes long during market stress.
```

Mechanism:

```text
1. wstETH cannot be redeemed quickly into ETH.
2. Market price of wstETH can trade below exchange-rate value.
3. Aave collateral quality deteriorates.
4. High-LTV positions approach liquidation.
5. Liquidators sell collateral into the same stressed liquidity.
6. Bad debt can appear if liquidation depth is insufficient.
7. Downstream protocols holding aTokens or building vaults on Aave inherit stress.
```

Why graph helps:

```text
The model can find all deployments and markets that use wstETH, not only Aave.
It can then rank them by exposure, LTV, chain, liquidity depth, and downstream use.
```

## Example: Circle / USDC Blast Radius

Path:

```text
entity:circle
  -> asset:usdc
  -> lending markets accepting USDC
  -> stable pools containing USDC
  -> vaults and strategies holding those positions
```

Questions the graph should answer:

```text
Which protocols accept USDC as collateral?
Which protocols only hold USDC as liquidity?
Which protocols depend on Circle and Chainlink at the same time?
Which pools contain both USDC and bridged USDC variants?
```

The answer should distinguish exposure types:

```text
accepts_collateral: high propagation
holds_liquidity: medium propagation
uses_as_reward_token: low propagation
```

## Example: Curve as Liquidity Backbone

Curve's protocol file describes Curve as a system. Pool files should later
describe concrete exposures.

Example planned nodes:

```text
protocol:curve
pool:curve.ethereum.3pool
pool:curve.ethereum.steth_eth
pool:curve.ethereum.crvusd_usdc
```

Potential cascade:

```text
stETH depeg
  -> Curve stETH/ETH pool imbalance
  -> price discovery distortion
  -> oracle/TWAP consumers affected
  -> lending liquidations or false health factors
  -> further forced selling
```

For Curve, the protocol-level risk is not only "Curve has risk". The important
point is that Curve pools are often price-discovery and liquidity backbones for
other protocols.

## Example Neo4j Queries

Blast radius for Lido:

```cypher
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected)
RETURN affected.uid AS affected, [n IN nodes(path) | n.uid] AS path
ORDER BY size(path), affected;
```

Active uses of a risk:

```cypher
MATCH (holder)-[rel:HAS_ACTIVE_RISK]->(:Risk {risk_id: "oracle_staleness"})
RETURN holder.uid, rel.deployment, rel.note;
```

Shared dependency:

```cypher
MATCH (d:Deployment)-[:DEPENDS_ON]->(:ExternalDependency {dependency_id: "circle"})
MATCH (d)-[:DEPENDS_ON]->(:ExternalDependency {dependency_id: "chainlink"})
RETURN d.uid, d.tvl_usd
ORDER BY d.tvl_usd DESC;
```

Weighted propagation:

```cypher
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected)
WITH affected, path,
     reduce(coeff = 1.0, r IN relationships(path) |
       coeff * coalesce(r.propagation_coeff, 1.0)
     ) AS propagated
RETURN affected.uid, propagated, [n IN nodes(path) | n.uid] AS path
ORDER BY propagated DESC;
```

## Current Limitations

The current model is a strong bootstrap, but not yet a complete exposure graph.

Known limitations and implementation tasks are tracked in `TODO.md`.

The immediate priority is to add the missing exposure layers and make cascade
questions answerable.

See `TODO.md` for the detailed roadmap.
