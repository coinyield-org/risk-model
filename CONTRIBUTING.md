# Contributing to `coinyield-data`

This repository is a data/model repo, not an app repo.

The source of truth is the risk model content under:

- `risk_model/protocols/`
- `risk_model/chains/`
- `risk_model/types/`
- `risk_model/taxonomy/`
- `risk_model/incidents/`
- `risk_model/attack_patterns/`

Neo4j is the query/index layer built from those files.

## Licensing of Contributions

This repository does not currently use a CLA.

Instead, contributions follow an **inbound = outbound** rule:

- if you contribute curated content / model data / documentation, your
  contribution is licensed under the repository's **CC BY-NC-SA 4.0** content
  license
- if you contribute tooling / scripts / infrastructure code, your contribution
  is licensed under the repository's **PolyForm Noncommercial 1.0.0** code
  license

By submitting a pull request, you confirm that:

1. you have the right to contribute the material
2. you are willing to license it under the repository's applicable license for
   that part of the project
3. you are not contributing third-party material unless you have the right to
   do so and its status is clearly documented

See:

- `LICENSE`
- `LICENSES.md`

## What contributors usually change

### 1. Update an existing protocol

Edit:

```text
risk_model/protocols/<slug>.md
```

Use YAML frontmatter for machine-readable fields and Markdown body for human-readable notes.

Typical changes:

- add/remove `active_risks`
- refine `dependencies`
- update `deployments`
- add audit metadata
- improve deployment-specific notes

### 2. Add a new protocol

Create:

```text
risk_model/protocols/<slug>.md
```

Requirements:

- stable `slug`
- at least one `types` entry
- at least one `deployment`
- `active_risks` must use existing taxonomy `risk_id`s
- dependency IDs should reference an existing protocol/chain where possible

If the protocol introduces a genuinely new risk, update the taxonomy first in:

```text
risk_model/taxonomy/protocol_risks.yaml
```

### 3. Update a chain

Edit:

```text
risk_model/chains/<chain>.md
```

Use this for chain-level structural risks only:

- reorg / halt / sequencer / censorship / validator concentration / bridge anchor dependence

Do not put protocol-admin risks on a chain unless the chain itself truly has that control surface.

### 4. Update token / asset risk taxonomy

Today first-class curated `assets/` files are not the main source of truth yet.

Use:

```text
risk_model/taxonomy/token_risks.yaml
```

and incident evidence under:

```text
risk_model/incidents/*.yaml
```

If you need asset-specific evidence, add `affected_assets` in incident files.

### 5. Add a new incident / hack

Create:

```text
risk_model/incidents/YYYY-MM-DD_short_slug.yaml
```

Read the full schema first:

```text
risk_model/incidents/README.md
```

Hard requirements:

- correct `incident:` ID
- `date`
- `event_type`
- `source_urls`
- `confidence`
- `risk_ids` from taxonomy
- `affected_protocols` only using known slugs
- `chains` only using known chain IDs

If you are not confident in the taxonomy mapping, keep `confidence: low` and explain uncertainty in `notes`.

## Local workflow

### Minimal workflow

From repo root:

```bash
make risk-graph-build
make neo4j-up
make neo4j-import
make neo4j-ci-check
```

If you want the full diagnostic report too:

```bash
make neo4j-check
```

### What each command does

```bash
make risk-graph-build   # regenerate generated/risk_model.cypher
make neo4j-up           # start local Neo4j
make neo4j-import       # load current model into Neo4j
make neo4j-ci-check     # fail-fast integrity checks used by CI
make neo4j-check        # broader diagnostic query pack
```

## Generated files

If your change affects the graph, you must commit:

```text
risk_model/neo4j/generated/risk_model.cypher
```

The CI will rebuild the graph and fail if the generated Cypher is stale.

## Pull request scope

Prefer one semantic change per PR:

- one protocol addition
- one chain fix
- one taxonomy change
- one incident batch

Avoid mixing:

- taxonomy redesign
- protocol additions
- incident backfills

in the same PR unless the changes are inseparable.

## PR checklist

Every PR should say:

1. what changed
2. why it changed
3. which files are source of truth
4. which `risk_id`s / slugs / chain IDs were touched
5. which primary sources support the change

For incident PRs, include:

- incident date
- affected protocol slugs
- risk IDs used
- confidence level

## CI contract

Every pull request runs a GitHub Action that:

1. installs Python + PyYAML
2. rebuilds `generated/risk_model.cypher`
3. fails if the generated file was not committed
4. starts local Neo4j in Docker
5. imports the graph
6. runs fail-fast integrity checks
7. uploads a full Neo4j check report as an artifact

The PR should be mergeable only after this passes.

## Review guidelines

Maintainers should reject PRs that:

- invent new `risk_id`s without taxonomy updates
- map incidents to guessed protocol slugs
- add stale generated files without matching source changes
- add chain-level risks that are really protocol-admin risks
- change multiple unrelated areas in one PR without a strong reason

## Naming and style

- use stable snake_case IDs
- keep protocol slugs lowercase with underscores
- keep incident filenames deterministic
- prefer specific notes over generic prose
- cite the mechanism, not just the headline

## Common examples

### Add a protocol risk

Edit:

```text
risk_model/protocols/aave_v3.md
```

Add:

```yaml
active_risks:
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "Why this is true for this deployment."
```

### Add an incident

Create:

```text
risk_model/incidents/2024-01-01_example.yaml
```

and include:

```yaml
affected_protocols:
  - aave_v3
risk_ids:
  - bad_debt_socialization
source_urls:
  - https://...
confidence: high
```

### Add a protocol without pool rows

This is valid.

Some protocol types, especially:

- `perps`
- `bridge`
- `messaging`

may be represented deployment-first rather than market-first.

You still add the protocol file in `risk_model/protocols/`.
The graph UI will fall back to deployment-level rendering when no `Market` nodes exist.
