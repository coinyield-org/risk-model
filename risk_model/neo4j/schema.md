# Risk Graph Schema

Version: `0.1`

## Design Rules

1. Source data stays in `risk_model/*`.
2. Neo4j stores queryable nodes and relationships derived from source data.
3. Every node has a globally unique `uid`.
4. Relationships point from the object consuming risk to the upstream dependency.
5. Relationship properties carry scope, exposure, propagation, confidence, and
   freshness when known.
6. Markdown remains the human-readable layer; graph properties are the
   machine-readable layer.

## Node Labels

All nodes also have the `RiskModelNode` label.

| Label | UID format | Meaning |
|---|---|---|
| `Protocol` | `protocol:<slug>` | Protocol-level object, e.g. `protocol:aave_v3`. |
| `Deployment` | `deployment:<protocol>.<chain>` | Protocol deployment on a chain. |
| `Chain` | `chain:<id>` | Chain / settlement layer. |
| `ProtocolType` | `type:<id>` | Protocol type profile, e.g. `type:lending`. |
| `Risk` | `risk:<risk_id>` | Stable risk taxonomy node. |
| `RiskCategory` | `risk_category:<id>` | Taxonomy category. |
| `Asset` | `asset:<symbol_slug>` | Asset referenced by dependencies. |
| `PricePair` | `price_pair:<base>_<quote>` | Oracle/feed pair such as `stETH/ETH`. |
| `Market` | `market:<pool_id>` | Pool / market imported from DeFiLlama yields data. |
| `ExternalDependency` | `dependency:<id>` | External service/entity not yet modeled as a first-class protocol/chain. |
| `AttackPattern` | `attack_pattern:<id>` | Multi-step attack pattern. |
| `Incident` | `incident:<YYYY-MM-DD_slug>` | A real-world DeFi incident used as evidence for taxonomy risks. |

## Relationship Types

| Relationship | Direction | Meaning |
|---|---|---|
| `HAS_DEPLOYMENT` | `Protocol -> Deployment` | Protocol has a chain deployment. |
| `DEPLOYED_ON` | `Deployment -> Chain` | Deployment runs on a chain. |
| `HAS_TYPE` | `Protocol -> ProtocolType` | Protocol belongs to a type profile. |
| `IN_CATEGORY` | `Risk -> RiskCategory` | Risk belongs to taxonomy category. |
| `HAS_BASE_RISK` | `ProtocolType/Chain -> Risk` | Structural risk inherited by type or chain. |
| `HAS_ACTIVE_RISK` | `Protocol/Deployment -> Risk` | Risk explicitly listed on a protocol node. |
| `DEPENDS_ON` | `Protocol/Deployment -> Protocol/Chain/ExternalDependency` | Upstream dependency from frontmatter. |
| `USES_ASSET` | `Protocol/Deployment -> Asset/PricePair` | Asset or price pair referenced by a dependency. |
| `INVOLVES_RISK` | `AttackPattern -> Risk` | Attack pattern contains a risk id. |
| `EVIDENCES_RISK` | `Incident -> Risk` | Incident provides evidence that this risk is real and calibrates likelihood/impact. |
| `INVOLVES_PROTOCOL` | `Incident -> Protocol` | Incident affected this protocol. |
| `INVOLVES_ASSET` | `Incident -> Asset` | Incident affected this asset. |
| `INVOLVES_CHAIN` | `Incident -> Chain` | Incident occurred on this chain. |

## Important Relationship Properties

These fields are optional. The importer fills what is available today and leaves
room for richer future `assets/` and `markets/` files.

| Property | Type | Meaning |
|---|---|---|
| `dependency_type` | string | Existing dependency type, e.g. `oracle_provider`, `issuer`, `bridge`. |
| `scope` | list/string | Chain/deployment scope from source data. |
| `assets` | list | Assets mentioned on the dependency edge. |
| `via` | list | Intermediate protocols/assets mentioned in source data. |
| `note` | string | Human note from frontmatter. |
| `propagation_coeff` | float | How much upstream impact propagates downstream. Defaults to `1.0` if absent. |
| `confidence` | string | `low`, `medium`, `high`; defaults can be added later. |
| `observed_at` | date string | Freshness timestamp for measured edge data. |
| `source_path` | string | File that produced the edge. |

## Direction Convention

Use consumer-to-dependency direction:

```text
deployment:aave_v3.ethereum -[:DEPENDS_ON]-> protocol:lido
deployment:aave_v3.ethereum -[:DEPENDS_ON]-> dependency:chainlink
deployment:aave_v3.ethereum -[:USES_ASSET]-> asset:wsteth
```

This makes upstream risk questions natural:

```cypher
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected)
RETURN path;
```

## Next Schema Step

Add first-class `Market` and curated `Asset` files:

```text
asset:wsteth -> protocol:lido
market:aave_v3.ethereum.wsteth -> asset:wsteth
market:aave_v3.ethereum.wsteth -> dependency:chainlink
```

That will let the graph distinguish protocol-level dependency from a precise
market exposure with LTV, liquidation threshold, TVL, caps, and oracle source.
