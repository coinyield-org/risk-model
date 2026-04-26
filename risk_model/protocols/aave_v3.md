---
slug: aave_v3
name: Aave V3
types: [lending]
deployments:
  - chain: ethereum
    tvl_usd: 15900000000
    since: 2023-01-27
  - chain: arbitrum
    tvl_usd: 3200000000
    since: 2023-03-23
  - chain: optimism
    tvl_usd: 900000000
    since: 2023-03-23
  - chain: polygon
    tvl_usd: 800000000
    since: 2023-03-23
  - chain: base
    tvl_usd: 700000000
    since: 2024-01-01
dependencies:
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
  - id: lido
    type: staking_protocol
    scope: [ethereum, arbitrum]
    assets: [wstETH, stETH]
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum, arbitrum]
    via: [kelp, renzo, etherfi]
  - id: layerzero
    type: bridge
    scope: [arbitrum, optimism, base]
    assets: [rsETH, ezETH]
  - id: circle
    type: issuer
    scope: all_deployments
    assets: [USDC]
active_risks:
  - risk_id: oracle_staleness
    deployment: arbitrum
    severity_override:
      likelihood: 4
      note: "Sequencer downtime on Arbitrum observed (Dec 2023)"
  - risk_id: withdrawal_queue_delay
    deployment: [ethereum, arbitrum]
    note: "wstETH/stETH collateral"
  - risk_id: bridge_dep
    deployment: [arbitrum, optimism, base]
    note: "rsETH/ezETH bridged via LayerZero"
audits:
  - firm: OpenZeppelin
    date: 2023-01
    url: ""
  - firm: Trail of Bits
    date: 2023-02
    url: ""
---

## Overview

Aave V3 — decentralized lending protocol. Users supply assets as collateral
and borrow against them. Core mechanics: overcollateralization, liquidation at
threshold, interest rate model with utilization kink.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Arbitrum deployment has additional surface:
- Sequencer dependency (uptime feed exists but not all oracle consumers check it correctly)
- Bridged collateral (rsETH, ezETH via LayerZero OFT — non-canonical backing)
- Different risk params vs mainnet (different supply caps, LTVs per asset)

## Key parameters (ethereum, as of 2026-01)

| Asset | LTV | Liq Threshold | Supply Cap | Oracle |
|-------|-----|---------------|------------|--------|
| wstETH | 80% | 82% | 1,200,000 | Chainlink wstETH/ETH |
| WBTC | 73% | 78% | 3,000 | Chainlink BTC/USD |
| USDC | 77% | 80% | 1,800,000,000 | Chainlink USDC/USD |
| rsETH | 72% | 75% | 8,000 | Chainlink rsETH/ETH |
