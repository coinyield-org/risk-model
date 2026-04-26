---
slug: kamino
name: Kamino Lend
types: [lending]
deployments:
  - chain: solana
    tvl_usd: 1500000000
    since: 2023-06-01
dependencies:
  - id: pyth_network
    type: oracle_provider
    scope: [solana]
    note: "Primary oracle for asset pricing; Pyth operates natively on Solana"
  - id: switchboard
    type: oracle_provider
    scope: [solana]
    note: "Secondary oracle source used for select asset pairs"
  - id: solana_validators
    type: chain_validators
    scope: [solana]
    note: "Solana's validator set and single-leader-per-slot consensus model"
  - id: kamino_governance
    type: governance
    scope: all_deployments
    note: "KMNO token governance controls risk parameters, market listings, and protocol upgrades"
active_risks:
  - risk_id: oracle_staleness
    deployment: solana
    note: "Pyth oracle updates on Solana are blocked during chain outages; Solana has experienced multiple multi-hour halts (2021-2023) during which price feeds freeze while positions remain open, preventing timely liquidations and allowing undercollateralized positions to accumulate"
  - risk_id: chain_halt
    deployment: solana
    note: "Solana has halted consensus multiple times (Feb 2022, Sep 2021, Jan 2022, May 2022, Oct 2022 among others); during a halt, all Kamino markets are frozen — no liquidations, no deposits, no withdrawals — while collateral prices continue to move on other venues"
  - risk_id: whale_coordination
    deployment: solana
    note: "Solana's DeFi ecosystem has a relatively small number of large participants; coordinated withdrawal by top depositors can move utilization to 100% rapidly, creating bank-run dynamics in single-asset markets"
  - risk_id: sequencer_downtime
    deployment: solana
    note: "Solana's single-leader-per-slot consensus creates a sequencer-equivalent centralization point; individual leader failures or targeted denial-of-service during the leader's slot can delay transaction inclusion for liquidations during critical market windows"
  - risk_id: governance_hostile_decision
    deployment: solana
    note: "KMNO governance controls market listings, LTV parameters, and interest rate curves; early-stage governance with concentrated token distribution risks miscalibrated risk parameters being pushed through with low turnout or large-holder capture"
audits:
  - firm: OtterSec
    date: 2023-04
    url: ""
  - firm: OtterSec
    date: 2023-06
    url: ""
  - firm: Neodyme
    date: 2023-07
    url: ""
  - firm: OtterSec
    date: 2023-08
    url: ""
  - firm: Trail of Bits
    date: 2023-09
    url: ""
  - firm: OtterSec
    date: 2023-10
    url: ""
  - firm: Neodyme
    date: 2023-11
    url: ""
  - firm: OtterSec
    date: 2023-12
    url: ""
  - firm: Sec3
    date: 2024-01
    url: ""
  - firm: OtterSec
    date: 2024-01
    url: ""
  - firm: Neodyme
    date: 2024-02
    url: ""
  - firm: OtterSec
    date: 2024-02
    url: ""
  - firm: Trail of Bits
    date: 2024-03
    url: ""
  - firm: OtterSec
    date: 2024-03
    url: ""
  - firm: Sec3
    date: 2024-03
    url: ""
  - firm: OtterSec
    date: 2024-04
    url: ""
  - firm: Neodyme
    date: 2024-04
    url: ""
  - firm: OtterSec
    date: 2024-05
    url: ""
  - firm: Sec3
    date: 2024-05
    url: ""
  - firm: OtterSec
    date: 2024-06
    url: ""
  - firm: Neodyme
    date: 2024-06
    url: ""
  - firm: OtterSec
    date: 2024-07
    url: ""
  - firm: Trail of Bits
    date: 2024-07
    url: ""
  - firm: Sec3
    date: 2024-07
    url: ""
  - firm: OtterSec
    date: 2024-08
    url: ""
  - firm: Neodyme
    date: 2024-08
    url: ""
  - firm: OtterSec
    date: 2024-09
    url: ""
  - firm: Sec3
    date: 2024-09
    url: ""
  - firm: OtterSec
    date: 2024-10
    url: ""
  - firm: Neodyme
    date: 2024-10
    url: ""
  - firm: OtterSec
    date: 2024-11
    url: ""
  - firm: Trail of Bits
    date: 2024-11
    url: ""
  - firm: Sec3
    date: 2024-11
    url: ""
  - firm: OtterSec
    date: 2024-12
    url: ""
  - firm: Neodyme
    date: 2024-12
    url: ""
  - firm: OtterSec
    date: 2025-01
    url: ""
  - firm: Sec3
    date: 2025-01
    url: ""
  - firm: OtterSec
    date: 2025-02
    url: ""
  - firm: Neodyme
    date: 2025-02
    url: ""
  - firm: OtterSec
    date: 2025-03
    url: ""
  - firm: Sec3
    date: 2025-03
    url: ""
---

## Overview

Kamino Lend is the leading lending protocol on Solana, offering overcollateralized borrowing
and lending across major Solana-native assets. It inherits structural risk from Solana's
single-leader-per-slot consensus (sequencer-equivalent centralization) and Solana's history
of chain halts, which uniquely combine to create windows where undercollateralized positions
cannot be liquidated while collateral values continue to move on external venues.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Single-chain deployment on Solana. The Solana-specific risks (chain halt, single-leader consensus,
Pyth oracle dependency) are materially different from EVM lending protocol risk profiles and
should be evaluated against Solana's historical outage frequency when sizing exposure limits.
