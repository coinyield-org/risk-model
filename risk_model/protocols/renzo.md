---
slug: renzo
name: Renzo (ezETH)
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 390000000
    since: 2023-12-01
  - chain: arbitrum
    tvl_usd: 0
    since: 2024-03-01
  - chain: base
    tvl_usd: 0
    since: 2024-03-01
  - chain: linea
    tvl_usd: 0
    since: 2024-04-01
dependencies:
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
  - id: ethereum_validators
    type: staking_protocol
    scope: [ethereum]
  - id: renzo_operator_set
    type: operator_set
    scope: [ethereum]
  - id: layerzero
    type: bridge
    scope: [arbitrum, base, linea]
    assets: [ezETH]
    note: OFT cross-chain ezETH
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    assets: [ezETH/ETH]
active_risks:
  - risk_id: validator_avs_slashing
    note: "EigenLayer AVS slashing applies to restaked ETH; new AVSs with unproven slashing conditions add tail risk"
  - risk_id: bridge_dep
    deployment: [arbitrum, base, linea]
    note: "Cross-chain ezETH is issued via LayerZero OFT; L2 ezETH backing depends on LayerZero bridge integrity"
  - risk_id: lst_lrt_depeg
    note: "April 2024: ezETH depegged to ~$0.97 when withdrawals were restricted and market sell pressure emerged; exchange rate vs market price divergence is a live risk"
  - risk_id: delegate_single_point_failure
    note: "Renzo operator set concentration; a small number of operators run the restaked validator set"
  - risk_id: withdrawal_queue_delay
    note: "EigenLayer withdrawal queue (multiple days) prevents rapid arbitrage of ezETH market depeg"
audits:
  - firm: Halborn
    date: 2024-03
    url: ""
---

## Overview

Renzo is a liquid restaking protocol issuing ezETH, backed by ETH restaked on
EigenLayer. Cross-chain ezETH is distributed via LayerZero OFT on Arbitrum, Base,
and Linea. In April 2024, ezETH depegged to approximately $0.97 during a period
when withdrawals were restricted and early unlock expectations drove market sell
pressure — demonstrating the concrete exchange-rate-vs-market risk for LRTs. TVL is
~$0.39B. Eleven Halborn audit reports are indexed from the Renzo-Protocol/contracts-public
repository.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Ethereum holds all underlying restaked ETH. L2 deployments (Arbitrum, Base, Linea)
hold bridged ezETH via LayerZero; their risk profiles include LayerZero bridge
failure on top of core LRT risks. The April 2024 depeg event primarily affected
L2 markets where exit was more constrained.
