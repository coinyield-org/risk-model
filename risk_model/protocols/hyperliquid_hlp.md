---
slug: hyperliquid_hlp
name: Hyperliquid HLP (Liquidity Provider Vault)
types: [perps]
deployments:
  - chain: hyperliquid_l1
    tvl_usd: 370000000
    since: 2024-01-01
    note: "HLP vault is modeled separately from the bridge / entry layer in hyperliquid.md; it acts as the market-maker counterparty to all perp trades on the exchange"
dependencies:
  - id: hyperliquid
    type: underlying_protocol
    scope: [hyperliquid_l1]
    note: "HLP vault is fully integrated into the Hyperliquid exchange; its PnL is a direct function of all trader activity on the platform"
  - id: hype_validators
    type: consensus
    scope: [hyperliquid_l1]
    note: "Hyperliquid L1 is a proprietary PoS chain; validators control both block production and the oracle price feed used by the perp engine"
  - id: hlp_vault_participants
    type: liquidity_provider
    scope: [hyperliquid_l1]
    note: "HLP shares represent proportional ownership of the vault's net asset value; large depositors can affect vault strategy and withdrawal dynamics"
active_risks:
  - risk_id: perp_funding_feedback
    deployment: hyperliquid_l1
    note: "HLP is the structural counterparty to all Hyperliquid perp trades; when aggregate trader positioning is net long, HLP is net short, and vice versa. Sustained one-sided market imbalance (e.g., large long bias during a bull run) creates directional P&L risk for the vault that cannot be hedged away within the platform"
  - risk_id: bad_debt_socialization
    deployment: hyperliquid_l1
    note: "When large leveraged positions generate losses exceeding the insurance fund, bad debt is socialized across HLP vault participants; this occurred during the March 2024 $JELLY incident where a whale's position forced significant mark-to-market losses on HLP depositors"
  - risk_id: oracle_staleness
    deployment: hyperliquid_l1
    note: "The Hyperliquid oracle price feed is produced by the Hyperliquid validator set — the same entities that validate blocks. This is not an independent oracle; validator collusion or a consensus failure can produce stale or manipulated prices that directly impact perp liquidation thresholds and HLP P&L"
  - risk_id: whale_concentration
    deployment: hyperliquid_l1
    note: "Large traders can open positions sized to move against HLP's structural short/long exposure, exploiting the vault's known directional bias at period-end or during low-liquidity windows; the March 2024 JELLY incident demonstrated this attack vector explicitly"
audits: []
---

## Overview

Hyperliquid HLP (HLP) is the liquidity provider vault on the Hyperliquid perpetual
exchange — a separate product from the exchange itself. HLP acts as the default
market-maker and counterparty to all perp trades on Hyperliquid L1. Depositors receive
HLP shares representing proportional ownership of the vault's NAV, which fluctuates with
trading P&L. Unlike external market makers, HLP cannot exit its counterparty role; it is
always the residual risk-taker for the platform's aggregate open interest.

## Type-specific risks

See `types/perps.md` for base risk profile.

## Deployment divergence

HLP is a single-chain product on Hyperliquid L1 — there are no multi-chain deployments.
The risk profile of this vault is inseparable from the Hyperliquid exchange risk (see
`hyperliquid.md`); chain-level risks (proprietary consensus, validator oracle, chain halt)
apply in full to HLP as well.

## Key parameters (hyperliquid_l1, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Vault type | Automated market-maker / structural counterparty |
| Depositor exposure | Net P&L of all Hyperliquid perp markets |
| Withdrawal | Subject to vault liquidity and open position sizing |
| Oracle | Hyperliquid validator set (not independent) |
| Insurance fund | Separate from HLP; absorbs liquidation shortfalls before socializing to HLP |
| Notable incident | Mar 2024 JELLY token manipulation — HLP forced to absorb $12M+ in losses |
