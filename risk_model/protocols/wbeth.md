---
slug: wbeth
name: Binance WBETH
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 8600000000
    since: 2023-04-27
  - chain: bnb
    tvl_usd: 0
    since: 2023-04-27
    note: "BNB Chain deployment; underlying ETH staked on Ethereum, WBETH bridged via Binance bridge"
dependencies:
  - id: binance
    type: custodian
    scope: all_deployments
    note: "Binance is sole issuer, custodian, and operator — runs all underlying ETH validators"
  - id: binance_beacon_chain
    type: underlying_chain
    scope: [bnb]
    note: "BNB Chain consensus layer underpins the BNB-side deployment"
  - id: binance_bridge
    type: bridge
    scope: [bnb]
    note: "WBETH cross-chain movement Ethereum ↔ BNB Chain routed through Binance-operated bridge"
active_risks:
  - risk_id: operator_concentration
    deployment: ethereum
    note: "Binance runs 100% of the validators backing WBETH; there is no operator diversification — any Binance validator incident (mass slashing, key leak, infra outage) affects the entire pool"
  - risk_id: custodian_risk
    deployment: ethereum
    note: "Binance is the sole issuer and redemption authority; regulatory action, insolvency, or operational failure at Binance would freeze or destroy the 1:1 ETH backing"
  - risk_id: minter_key_leak
    deployment: [ethereum, bnb]
    note: "Binance controls the mint/burn admin keys; compromise allows unauthorized minting and backing dilution across both chains"
  - risk_id: issuer_corporate_risk
    deployment: all_deployments
    note: "Binance faces ongoing regulatory scrutiny across multiple jurisdictions (DOJ settlement 2023, ongoing monitoring); a material adverse regulatory event could disrupt minting, redemptions, or the exchange itself, which underpins WBETH liquidity"
  - risk_id: exchange_rate_vs_market_depeg
    deployment: [ethereum, bnb]
    note: "WBETH trades at small discount/premium; during Binance stress events (e.g., large withdrawals), secondary market liquidity thins and the peg can dislocate meaningfully before arbitrage restores it"
  - risk_id: bridge_dep
    deployment: bnb
    note: "WBETH on BNB Chain relies on the Binance-operated bridge; bridge pause or exploit would strand WBETH on BNB Chain away from its ETH backing"
audits:
  - firm: SlowMist
    date: 2023-04
    url: ""
  - firm: PeckShield
    date: 2023-05
    url: ""
---

## Overview

WBETH (Wrapped Beacon ETH) is Binance's liquid staking token issued when users stake
ETH through Binance's staking product. It accrues ETH staking rewards in exchange
rate terms (similar to wstETH). Binance operates all underlying validators, making
this a fully custodial LST — the DeFi-native equivalent of a centralized staking
receipt. It is deployed on both Ethereum and BNB Chain, with the BNB Chain version
bridged via Binance's own cross-chain infrastructure.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

BNB Chain deployment is a bridged representation:
- Underlying ETH validators are on Ethereum beacon chain; the BNB Chain token is
  not independently backed.
- Binance controls the bridge and can pause cross-chain movement unilaterally.
- BNB Chain has different finality and validator set characteristics; smart contract
  execution risk differs from Ethereum mainnet.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Operator | Binance (sole) |
| Redemption method | Via Binance platform (centralized) |
| Staking APY source | Ethereum beacon chain rewards |
| On-chain enforceability | None — Binance custodian model |
| Proof of reserves | Binance PoR (centralized attestation) |
