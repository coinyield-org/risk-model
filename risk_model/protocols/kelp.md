---
slug: kelp
name: Kelp DAO (rsETH)
types: [lrt]
deployments:
  - chain: ethereum
    tvl_usd: 1500000000
    since: 2023-12-01
  - chain: arbitrum
    tvl_usd: 50000000
    since: 2024-03-01
  - chain: base
    tvl_usd: 30000000
    since: 2024-04-01
  - chain: optimism
    tvl_usd: 20000000
    since: 2024-05-01
dependencies:
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    note: "rsETH backing is ETH restaked through EigenLayer; all EigenLayer slashing and AVS risks are inherited"
  - id: lido
    type: staking_protocol
    scope: [ethereum]
    assets: [stETH]
    note: "stETH is a primary LST input for rsETH minting"
  - id: stader_labs
    type: staking_protocol
    scope: [ethereum]
    assets: [ETHx]
    note: "ETHx accepted as LST input"
  - id: frax_finance
    type: staking_protocol
    scope: [ethereum]
    assets: [sfrxETH]
    note: "sfrxETH accepted as LST input"
  - id: layerzero
    type: bridge
    scope: [arbitrum, base, optimism]
    assets: [rsETH]
    note: "rsETH is bridged to L2s via LayerZero OFT; cross-chain rsETH is not canonically backed on destination chains"
  - id: chainlink
    type: oracle_provider
    scope: all_deployments
    assets: [rsETH/ETH, stETH/ETH]
active_risks:
  - risk_id: validator_avs_slashing
    deployment: ethereum
    note: "rsETH backing includes ETH restaked in EigenLayer AVSs; slashing events on any AVS reduce rsETH's ETH backing below par. Kelp curates the operator set but cannot prevent downstream AVS slashing once operators are opted in"
  - risk_id: bridge_dep
    deployment: [arbitrum, base, optimism]
    note: "rsETH on L2s is bridged via LayerZero OFT; if LayerZero is exploited or paused, L2 rsETH loses canonical backing — L2 holders cannot redeem against Ethereum mainnet reserves directly. This is the studied withdrawal_queue_blocking attack pattern for LRT cross-chain deployments"
  - risk_id: lst_lrt_depeg
    deployment: all
    note: "rsETH can trade at a discount to its underlying ETH exchange rate during stress; the EigenLayer withdrawal queue (7+ days) prevents arbitrageurs from closing the gap, allowing sustained depeg"
  - risk_id: delegate_single_point_failure
    deployment: ethereum
    note: "Kelp curates the operator set for restaking; concentration in a small number of node operators creates correlated slashing exposure — a single large operator incident affects a disproportionate share of rsETH backing"
  - risk_id: withdrawal_queue_delay
    deployment: [ethereum]
    note: "rsETH redemptions pass through EigenLayer's withdrawal queue (minimum 7 days plus Ethereum validator exit queue); during stress, depeg cannot be arbitraged closed and liquidity on secondary markets may be the only exit"
audits:
  - firm: Sigma Prime
    date: 2024-01
    url: ""
  - firm: Sigma Prime
    date: 2024-03
    url: ""
  - firm: Sigma Prime
    date: 2024-06
    url: ""
---

## Overview

Kelp DAO issues rsETH, a liquid restaking token that wraps staked ETH (via stETH, ETHx, sfrxETH)
and restakes it through EigenLayer. rsETH holders receive both Ethereum staking yield and EigenLayer
restaking points/rewards, but bear the additional slashing risk from AVS opt-ins curated by Kelp.
rsETH is bridged to Arbitrum, Base, and Optimism via LayerZero OFT, creating non-canonical cross-chain
exposure studied as a structural risk in LRT bridge attack patterns.

## Type-specific risks

See `types/lrt.md` for base risk profile.

## Deployment divergence

Ethereum mainnet holds all real backing; L2 deployments (Arbitrum, Base, Optimism) hold bridged
rsETH via LayerZero OFT with no independent collateral on those chains. L2 rsETH holders face an
additional bridge dependency layer not present for mainnet holders: LayerZero failure would strand
L2 rsETH without a direct redemption path. Withdrawal queue delays compound differently on L2
because the queue operates only on Ethereum mainnet.

## Key parameters (as of 2026-01)

| Parameter | Value |
|-----------|-------|
| LST inputs | stETH, ETHx, sfrxETH |
| Restaking layer | EigenLayer |
| Operator selection | Kelp-curated set |
| L2 bridge | LayerZero OFT |
| EigenLayer withdrawal delay | 7+ days (plus validator exit queue) |
