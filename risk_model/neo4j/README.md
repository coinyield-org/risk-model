# Neo4j Risk Graph

This directory contains the Neo4j layer for `risk_model`.

The Markdown/YAML files under `risk_model/protocols`, `risk_model/types`,
`risk_model/chains`, `risk_model/taxonomy`, and `risk_model/attack_patterns`
remain the source of truth. Neo4j is the query/index layer used to answer graph
questions: blast radius, shared dependencies, recursive dependency chains, and
feedback loops.

## Files

- `schema.md` - graph model, node labels, relationship types, and ID rules.
- `constraints.cypher` - uniqueness constraints and indexes.
- `queries.cypher` - useful starter queries for exploration.
- `checks.cypher` - runnable verification and diagnostic queries.
- `import_risk_model.py` - builds `generated/risk_model.cypher` from the current
  risk model files.
- `load_generated.sh` - loads generated Cypher into the local Docker Compose
  Neo4j service.
- `generated/risk_model.cypher` - generated import script. Regenerate it after
  changing source data.

## Generate Import Cypher

Use a Python environment with PyYAML installed.

```bash
/opt/homebrew/anaconda3/bin/python risk_model/neo4j/import_risk_model.py
```

Or, if your default Python has PyYAML:

```bash
python3 risk_model/neo4j/import_risk_model.py
```

## Local Neo4j

Create a local env file if you want to override defaults:

```bash
cp .env.example .env
```

Start Neo4j:

```bash
make neo4j-up
```

Build and import the graph:

```bash
make neo4j-import
```

Open `http://localhost:7474` and run queries from `queries.cypher`.

Run verification and diagnostic queries:

```bash
make neo4j-check
```

Default credentials:

```text
user: neo4j
password: password
```

Neo4j stores local data under `.neo4j/`, which is gitignored.

Important: `NEO4J_AUTH` only initializes the password when the database volume is
first created. If you change credentials after `.neo4j/data` already exists,
clear the local volume or change the password through Neo4j.

Useful commands:

```bash
make risk-graph-build  # regenerate generated/risk_model.cypher
make neo4j-import      # regenerate and load into local Neo4j
make neo4j-ci-check    # fail-fast integrity checks used by CI
make neo4j-check       # run risk_model/neo4j/checks.cypher
make neo4j-shell       # open cypher-shell inside the container
make neo4j-logs        # follow Neo4j logs
make neo4j-down        # stop local Neo4j
```

## Mental Model

Edges point from consumer to dependency:

```text
deployment:aave_v3.ethereum -[:DEPENDS_ON]-> protocol:lido
deployment:aave_v3.ethereum -[:USES_ASSET]-> asset:wsteth
deployment:aave_v3.ethereum -[:HAS_ACTIVE_RISK]-> risk:oracle_staleness
```

To ask "what is affected if Lido has a problem", traverse incoming dependency
edges:

```cypher
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected)
RETURN path;
```

This is the main difference from the Markdown files: the graph can explain the
path of impact, not only that two objects are related.
