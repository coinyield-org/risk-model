---
id: oracle_staleness
name: "Staleness (heartbeat violated)"
category: oracle
applies_to: [lending, cdp, dex, perps, yield_aggregator, lst, lrt]
severity:
  likelihood: 3
  impact: 4
  derived: 12
  scoring_policy_version: "0.1"
related_risks:
  - deviation_threshold_too_wide
  - sequencer_uptime_feed_missing
  - fallback_oracle_misconfig
incidents: []
---

## Definition

The oracle feed stops updating. The protocol continues to use the last
known value as current.

## Mechanism

A Chainlink feed updates under one of two conditions: (a) price changed by ≥ deviation threshold, (b) heartbeat interval expired. If neither condition is met (price "doesn't move" by oracle standards, but actually changed) — the feed is stale.

On L2: sequencer downtime = all oracle feeds stale, but transactions continue to execute. Without a sequencer uptime check the protocol accepts a stale price as fresh.

## Preconditions

- Heartbeat > characteristic time of the asset's price movement
- Absence of sequencer uptime feed (on L2)
- No on-chain staleness check in the protocol

## Impact path

```
oracle_staleness → collateral mispriced → borrow at wrong LTV → bad debt
oracle_staleness → stale low price → liquidation false trigger
oracle_staleness → stale high price → under-liquidation → bad debt
```

## Defenses

- `block.timestamp - updatedAt < maxStaleness` check on every oracle read
- Sequencer uptime feed (Chainlink L2 sequencer check)
- Fallback oracle with an independent source

## Incidents

_(none indexed yet)_
