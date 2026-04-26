---
slug: drift
name: Drift Protocol
types: [perps]
deployments:
  - chain: solana
dependencies:
  - id: pyth_network
    type: oracle_provider
    scope: all_deployments
    note: "Drift mark prices and liquidation thresholds rely on external oracle updates from Pyth"
  - id: solana_validators
    type: infrastructure
    scope: all_deployments
    note: "Drift inherits Solana liveness, congestion, and transaction-inclusion behavior for liquidations and settlements"
  - id: drift_liquidators
    type: keeper
    scope: all_deployments
    note: "Liquidation performance depends on external bots being online and economically willing to clear unhealthy accounts during volatility"
  - id: drift_governance
    type: governance
    scope: all_deployments
    note: "Governance and admin signers can change collateral listings, risk parameters, and upgrade paths"
active_risks:
  - risk_id: oracle_staleness
    deployment: solana
    note: "Pyth update lag or Solana liveness issues can leave Drift using stale mark prices exactly when leveraged positions need fast liquidation"
  - risk_id: chain_halt
    deployment: solana
    note: "A Solana halt freezes order placement, settlement, and liquidation while off-chain prices continue to move, creating direct bad-debt risk for perp markets"
  - risk_id: single_keeper_dependency
    deployment: solana
    note: "Liquidation throughput depends on a relatively small set of specialized keepers; if they fail or stand down during stress, unhealthy positions remain open"
  - risk_id: illiquid_collateral_liquidation
    deployment: solana
    note: "Thin collateral markets on Solana can make forced exits unprofitable or impossible at oracle marks; the May 2022 incident demonstrated that undercollateralized accounts can outrun liquidation depth"
  - risk_id: insurance_fund_depletion
    deployment: solana
    note: "Perp bad debt is first absorbed by Drift's risk buffers and insurance mechanisms; repeated liquidation shortfalls can deplete that buffer and force socialization"
  - risk_id: governance_signer_key_leak
    deployment: solana
    note: "Compromise of governance/admin signers can change collateral whitelists, risk parameters, or upgrade paths; the April 2026 incident is a direct precedent for this control surface"
audits: []
---

## Overview

Drift Protocol is a Solana-native perpetual futures exchange. Traders post collateral,
open leveraged long/short positions, and settle P&L against protocol liquidity and risk
buffers. The critical surfaces are mark-price integrity, liquidation throughput, Solana
liveness, and governance control over market parameters.

## Type-specific risks

See `types/perps.md` for base risk profile.

## Deployment divergence

Single-chain deployment on Solana. That makes Drift materially different from EVM perps:

- Solana outages block liquidations and settlement at the chain level
- Pyth oracle updates and Solana liveness are correlated operational dependencies
- Liquidation capacity depends on specialized keeper infrastructure rather than a deep, commoditized Ethereum bot market

## Key parameters

| Parameter | Detail |
|-----------|--------|
| Chain | Solana |
| Product | Perpetual futures |
| Mark price source | Pyth Network |
| Liquidation model | External keeper / liquidator bots |
| Loss absorber | Insurance fund / protocol buffers before socialization |
| Notable incident | May 2022 liquidation shortfall; Apr 2026 governance signer compromise |
