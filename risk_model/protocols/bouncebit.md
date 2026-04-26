---
slug: bouncebit
name: BounceBit CeDeFi Yield
types: [synthetic]
deployments:
  - chain: ethereum
    tvl_usd: 360000000
    since: 2024-04-01
    note: "BounceBit operates on a proprietary EVM-compatible chain; Ethereum is the entry/exit point for user deposits"
dependencies:
  - id: mainnet_digital
    type: custodian
    scope: all_deployments
    note: "Mainnet Digital holds underlying BTC/USDT custody for the basis-trading strategy; off-chain custodian with no on-chain enforceability"
  - id: binance_okx
    type: cex_venue
    scope: all_deployments
    note: "Funding rate capture is executed on Binance and OKX perpetual markets; strategy yield is entirely dependent on sustained positive funding rates"
  - id: bouncebit_validators
    type: consensus
    scope: all_deployments
    note: "BounceBit runs a proprietary PoS chain for settlement; validator set is permissioned and controlled by the BounceBit Foundation"
active_risks:
  - risk_id: custodian_risk
    deployment: all
    note: "Mainnet Digital custodian holds 100% of the BTC/USDT backing the BounceBit yield strategy off-chain; insolvency, regulatory seizure, or misappropriation at Mainnet Digital results in direct loss with no on-chain recourse — analogous to the Celsius/BlockFi custody risk pattern"
  - risk_id: perp_funding_feedback
    deployment: all
    note: "BounceBit yield depends on persistent positive perpetual funding rates on Binance/OKX; when market sentiment shifts and funding rates turn negative for extended periods, the strategy generates losses rather than yield, creating adverse P&L for depositors"
  - risk_id: issuer_corporate_risk
    deployment: all
    note: "The BounceBit Foundation controls the proprietary chain, smart contracts, and yield distribution mechanics; regulatory action against the foundation, key personnel departure, or business failure would halt operations with limited recourse for depositors"
  - risk_id: chain_halt
    deployment: all
    note: "BounceBit operates on a proprietary PoS chain with a permissioned validator set; a consensus failure, validator coordination failure, or infrastructure outage halts withdrawals and on-chain settlements with no fallback to a decentralized chain"
  - risk_id: oracle_staleness
    deployment: all
    note: "Yield accrual and NAV calculation depend on off-chain funding rate data from CEX APIs; stale or manipulated feed data could misrepresent strategy performance and delay accurate depositor P&L accounting"
audits:
  - firm: PeckShield
    date: 2024-04
    url: ""
  - firm: BlockSec
    date: 2024-05
    url: ""
---

## Overview

BounceBit is a CeDeFi yield platform that captures Bitcoin perpetual futures funding
rates through a basis-trading strategy. User BTC is held in custody by Mainnet Digital
and deployed as collateral for short perp positions on Binance and OKX, earning funding
rate income. BounceBit wraps this strategy in an EVM-compatible proprietary chain with
its own validator set, issuing yield-bearing tokens to depositors. The protocol's yield
is entirely dependent on sustained positive funding rates and the integrity of the
off-chain custodian relationship.

## Type-specific risks

See `types/synthetic.md` for base risk profile.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Custody model | Off-chain (Mainnet Digital) |
| Yield source | BTC/USDT perp funding rates on Binance, OKX |
| Chain type | Proprietary EVM PoS (permissioned validators) |
| Audit coverage | 2 PDFs (PeckShield, BlockSec) |
| On-chain enforceability | Limited — custodian relationship is off-chain |
