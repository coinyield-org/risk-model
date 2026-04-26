---
version: 0.1
updated: 2026-04-21
---

# Scoring Policy

## Severity model

Severity = f(likelihood, impact). Two-dimensional — never collapse to single score prematurely.

```
severity:
  likelihood: 1-5   # 1=theoretical, 3=observed in similar protocol, 5=actively exploited
  impact:     1-5   # 1=dust, 3=partial TVL loss, 5=total protocol drain or systemic cascade
  derived:    L * I  # 1-25, used for sorting only
```

## Likelihood scale

| Score | Meaning |
|-------|---------|
| 1 | Theoretical only, no PoC, requires exotic conditions |
| 2 | PoC exists or preconditions plausible |
| 3 | Observed in comparable protocol / similar TVL range |
| 4 | Observed in this exact protocol type, this chain |
| 5 | Actively exploited or near-miss in last 12 months |

## Impact scale

| Score | Meaning |
|-------|---------|
| 1 | < $100K loss or single-user impact |
| 2 | $100K–$1M or significant UX degradation |
| 3 | $1M–$10M or temporary protocol freeze |
| 4 | $10M–$100M or prolonged market freeze |
| 5 | > $100M, systemic contagion, or permanent loss of peg |

## Propagation

When scoring a risk on a dependency edge, apply damping coefficient from `schema.md`:

```
effective_impact = impact * edge.propagation_coeff
```

## Versioning

This file is versioned. Risk scores in node YAMLs reference `scoring_policy_version`.
Changing this file does not retroactively change historical scores — bump the version.
