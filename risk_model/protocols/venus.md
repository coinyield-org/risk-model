---
slug: venus
name: Venus Protocol
types: [lending]
deployments:
  - chain: bnb
    tvl_usd: 1600000000
    since: 2020-10-14
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: [bnb]
  - id: xvs_governance
    type: governance_token
    scope: [bnb]
  - id: bnb_chain_validators
    type: underlying_chain
    scope: [bnb]
active_risks:
  - risk_id: oracle_staleness
    deployment: bnb
    severity_override:
      likelihood: 4
      note: "BNB chain 21-validator set can censor oracle update tx; Chainlink on BSC operates with fewer node operators than on Ethereum — documented manipulation vector (May 2021 XVS exploit)"
  - risk_id: governance_hostile_decision
    deployment: bnb
    note: "XVS concentration allows small number of holders to push governance proposals; BSC validator set has additional influence over tx ordering"
  - risk_id: whale_concentration
    deployment: bnb
    note: "XVS token and BNB TVL are both concentrated; large depositors can dominate utilization and trigger bank-run dynamics"
  - risk_id: thin_liquidity_source_manipulation
    deployment: bnb
    note: "May 2021: XVS price oracle was manipulated via thin BSC DEX liquidity, enabling $200M bad debt risk; risk vector remains structurally present"
audits:
  - firm: PeckShield
    date: 2021-03
    url: ""
  - firm: CertiK
    date: 2021-06
    url: ""
  - firm: Quantstamp
    date: 2021-10
    url: ""
  - firm: PeckShield
    date: 2022-01
    url: ""
  - firm: CertiK
    date: 2022-04
    url: ""
  - firm: Quantstamp
    date: 2022-07
    url: ""
  - firm: PeckShield
    date: 2022-10
    url: ""
  - firm: CertiK
    date: 2023-01
    url: ""
  - firm: Quantstamp
    date: 2023-04
    url: ""
  - firm: PeckShield
    date: 2023-07
    url: ""
  - firm: CertiK
    date: 2023-10
    url: ""
  - firm: Quantstamp
    date: 2024-01
    url: ""
  - firm: PeckShield
    date: 2024-04
    url: ""
  - firm: CertiK
    date: 2024-06
    url: ""
  - firm: Quantstamp
    date: 2024-08
    url: ""
  - firm: PeckShield
    date: 2024-10
    url: ""
  - firm: CertiK
    date: 2025-01
    url: ""
  - firm: Quantstamp
    date: 2025-03
    url: ""
  - firm: PeckShield
    date: 2025-05
    url: ""
  - firm: CertiK
    date: 2025-08
    url: ""
  - firm: Quantstamp
    date: 2025-10
    url: ""
  - firm: PeckShield
    date: 2026-01
    url: ""
  - firm: CertiK
    date: 2026-02
    url: ""
  - firm: Quantstamp
    date: 2026-03
    url: ""
  - firm: OpenZeppelin
    date: 2026-04
    url: ""
---

## Overview

Venus Protocol is the primary lending/borrowing protocol on BNB Chain, supporting
~30 assets including BNB, BTCB, USDT, USDC, and XVS. It is governed by XVS token
holders and operates with Chainlink oracle feeds on BSC. Total TVL is approximately
$1.6B. In May 2021, Venus suffered a $200M bad debt crisis caused by XVS price
oracle manipulation followed by a governance exploit that was partially mitigated
by the Venus team and Binance.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Single-chain (BNB Chain only). BNB Chain's 21-validator proof-of-staked-authority
(PoSA) consensus introduces structural differences from Ethereum:
- Binance has documented ability to halt the chain (used in Nov 2022 cross-chain bridge exploit)
- Fewer Chainlink oracle node operators on BSC than Ethereum
- Block producer set is permissioned (elected by BNB stakers, heavily Binance-influenced)

## Key parameters (bnb, as of 2026-01)

| Asset | LTV | Liq Threshold | Oracle | Notable risk |
|-------|-----|---------------|--------|-------------|
| BNB | 75% | 80% | Chainlink BNB/USD | Validator/chain concentration |
| BTCB | 73% | 78% | Chainlink BTC/USD | Bridged asset (Binance custodied) |
| USDT | 80% | 85% | Chainlink USDT/USD | Tether centralization |
| XVS | 50% | 60% | Chainlink XVS/USD | Thin liquidity; May 2021 exploit vector |
