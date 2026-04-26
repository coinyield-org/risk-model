---
slug: pendle
name: Pendle Finance
types: [yield_trading]
deployments:
  - chain: ethereum
    tvl_usd: 900000000
    since: 2021-06-17
  - chain: arbitrum
    tvl_usd: 400000000
    since: 2023-03-01
  - chain: bnb
    tvl_usd: 100000000
    since: 2023-06-01
  - chain: base
    tvl_usd: 60000000
    since: 2024-01-01
  - chain: optimism
    tvl_usd: 40000000
    since: 2024-01-01
dependencies:
  - id: lido
    type: staking_protocol
    scope: [ethereum, arbitrum]
    assets: [stETH, wstETH]
  - id: etherfi
    type: staking_protocol
    scope: [ethereum]
    assets: [eETH, weETH]
  - id: kelp
    type: restaking_protocol
    scope: [ethereum]
    assets: [rsETH]
  - id: ethena
    type: synthetic_protocol
    scope: [ethereum, arbitrum]
    assets: [sUSDe]
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: amm_lps
    type: liquidity_provider
    scope: all_deployments
active_risks:
  - risk_id: deep_chain_yield_trading
    deployment: [ethereum, arbitrum]
    note: "PT/YT of rsETH = 4-layer dependency: Ethereum → EigenLayer → Kelp → rsETH → Pendle"
  - risk_id: timelock_skew_cross_chain
    deployment: all_deployments
    note: "Maturity cliff: PT price converges to par at expiry — price discontinuity if pool is not migrated"
  - risk_id: incentive_end_liquidity_flight
    deployment: all_deployments
    note: "Pool migration gap at maturity: LPs must migrate to next-maturity pool; dead window creates liquidity vacuum"
  - risk_id: underlying_protocol_pause
    deployment: [ethereum, arbitrum]
    note: "Pendle PT/YT halts redemption if underlying yield source (Lido, Kelp, Ethena) pauses"
  - risk_id: oracle_staleness
    deployment: all_deployments
    note: "YT pricing requires implied APY oracle; no standard Chainlink feed — bespoke TWAP prone to manipulation"
audits:
  - firm: Ackee
    date: 2023-01
    url: ""
  - firm: Trail of Bits
    date: 2023-03
    url: ""
  - firm: Dedaub
    date: 2023-06
    url: ""
  - firm: ChainSecurity
    date: 2023-09
    url: ""
  - firm: OpenZeppelin
    date: 2024-01
    url: ""
  - firm: Spearbit/Cantina
    date: 2024-03
    url: ""
---

## Overview

Pendle Finance is a yield-trading protocol that splits yield-bearing assets into
Principal Tokens (PT) and Yield Tokens (YT), each tradeable on Pendle's AMM.
PT holders receive par value at maturity; YT holders receive all yield generated
until maturity. The protocol supports stETH, eETH, rsETH, sUSDe and other
yield-bearing assets across five chains with ~$1.5B TVL.

## Type-specific risks

See `types/yield_trading.md` for base risk profile.

## Deployment divergence

Arbitrum deployment carries additional surface:
- Bridged underlying assets (rsETH, ezETH via LayerZero) add a bridge-dep layer
- Sequencer dependency: stale oracle prices served during sequencer downtime
- Thinner AMM liquidity per pool than Ethereum mainnet

BNB/Base/Optimism deployments are smaller and have fewer audited integrations.

## Key parameters (ethereum, as of 2026-01)

| Pool | Underlying | Maturity | Implied APY oracle | Dependency depth |
|------|-----------|----------|-------------------|-----------------|
| PT-rsETH | rsETH (Kelp) | 3–6 months | Bespoke TWAP | 4 layers |
| PT-weETH | eETH (EtherFi) | 3–6 months | Bespoke TWAP | 3 layers |
| PT-sUSDe | sUSDe (Ethena) | 1–6 months | Bespoke TWAP | 2 layers |
| PT-stETH | stETH (Lido) | 3–6 months | Bespoke TWAP | 2 layers |
