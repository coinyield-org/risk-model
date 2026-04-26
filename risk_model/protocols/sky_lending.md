---
slug: sky_lending
name: Sky Lending (MakerDAO / Sky)
types: [cdp]
deployments:
  - chain: ethereum
    tvl_usd: 5300000000
    since: 2017-12-17
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: [ethereum]
    note: "Chainlink feeds all collateral prices through OSM (Oracle Security Module) with a 1-hour delay"
  - id: circle
    type: issuer
    scope: [ethereum]
    assets: [USDC]
    note: "PSM holds large USDC reserves (~50% of DAI/USDS backing at times); Circle blacklist or regulatory freeze would impair peg stability"
  - id: spark_protocol
    type: lending_arm
    scope: [ethereum]
    note: "Spark is the native lending frontend for Sky/MakerDAO; it is a major consumer of the protocol's credit capacity"
  - id: mkr_sky_governance
    type: governance
    scope: [ethereum]
    note: "MKR/SKY token holders vote on all system parameters including collateral types, debt ceilings, stability fees, and PSM configurations"
active_risks:
  - risk_id: governance_hostile_decision
    deployment: ethereum
    note: "MKR governance controls every critical parameter in the system — adding/removing collateral types, setting debt ceilings, adjusting stability fees, and authorizing new modules. A hostile or low-turnout governance vote could enable risky collateral, drain the Surplus Buffer, or fundamentally alter the peg mechanism"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "The Oracle Security Module (OSM) deliberately delays price feed updates by 1 hour to allow emergency shutdown before a price manipulation can be exploited. However, this design means the protocol operates on 1-hour-old prices — a rapid flash crash in collateral value that resolves within 1 hour will not trigger liquidations, but a sustained crash will liquidate at stale prices, potentially at a loss"
  - risk_id: concentrated_pool_dependency
    deployment: ethereum
    note: "The Peg Stability Module (PSM) holds USDC as primary backing asset; at peak this represented ~50% of all DAI/USDS collateral. Circle's operational risk (blacklist, freeze, regulatory action) or USDC depeg would directly impair Sky's peg mechanism"
  - risk_id: whale_concentration
    deployment: ethereum
    note: "MKR token supply is highly concentrated among early holders and venture investors; a coordinated vote or large MKR acquisition could swing governance on critical proposals with low voter turnout"
  - risk_id: issuer_corporate_risk
    deployment: ethereum
    note: "Sky's heavy PSM reliance on USDC creates a transitive dependency on Circle, a US-regulated entity; Circle sanctions enforcement or USDC operational failure propagates directly into Sky's collateral base"
audits:
  - firm: Trail of Bits
    date: 2023-06
    url: ""
  - firm: Certora
    date: 2023-08
    url: ""
  - firm: ChainSecurity
    date: 2022-11
    url: ""
---

## Overview

Sky Lending (formerly MakerDAO) is the original CDP protocol on Ethereum, allowing
users to deposit collateral and mint DAI (now USDS under the Sky rebrand) at a
stability fee. The system uses the OSM oracle system with a deliberate 1-hour delay
as a manipulation buffer, a Surplus Buffer for first-loss coverage, and a PSM for
direct USDC↔DAI arbitrage to maintain the peg. Spark Protocol serves as the primary
lending interface for the Sky ecosystem. With over $5B in debt, governance decisions
have systemic implications across DeFi.

## Type-specific risks

See `types/cdp.md` for base risk profile.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Oracle delay (OSM) | 1 hour |
| Stability fee | Varies by collateral vault type (0.5%–8% typical) |
| PSM USDC capacity | Variable debt ceiling set by governance |
| Liquidation ratio (ETH-A) | 150% |
| Surplus Buffer | ~$50–100M (governance-set target) |
| Governance token | MKR (legacy) / SKY (rebrand) |
| Minimum governance delay | 48-hour governance cycle on most executive spells |
