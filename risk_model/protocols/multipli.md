---
slug: multipli
name: Multipli.fi
types: [yield_aggregator]
deployments:
  - chain: ethereum
    tvl_usd: 370000000
    since: 2024-01-01
    note: "Exact launch date and chain not publicly confirmed; assumed Ethereum mainnet based on LRT dependency stack"
dependencies:
  - id: eigenlayer
    type: restaking_protocol
    scope: [ethereum]
    note: "Multipli strategies layer on top of EigenLayer restaking as part of the points/yield stack"
  - id: lrt_protocols
    type: underlying_protocol
    scope: [ethereum]
    note: "LRT protocols (e.g., EtherFi, Kelp, Renzo) form the yield-generating base layer that Multipli wraps"
  - id: multipli_team
    type: governance
    scope: [ethereum]
    note: "Strategy parameters, allocation targets, and point-farming mechanics are controlled by the Multipli team; no DAO or timelock identified"
active_risks:
  - risk_id: deep_chain_yield_trading
    deployment: ethereum
    note: "Multipli stacks points farming on top of LRT positions, which themselves sit on EigenLayer restaking, which sits on Ethereum staking — creating a 4+ layer dependency chain where each layer carries independent smart contract, slashing, and liquidity risk; a failure at any layer propagates upward to Multipli depositors"
  - risk_id: incentive_end_liquidity_flight
    deployment: ethereum
    note: "Multipli TVL is primarily driven by LRT points and airdrop expectations from EigenLayer and LRT protocol campaigns; once points campaigns conclude and airdrops are distributed, mercenary capital is likely to exit, leaving remaining depositors with illiquid or unexited positions"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "No public audits have been identified for Multipli smart contracts; the absence of an audit means that contract upgrade authority or admin keys represent an unquantified risk — a compromised or malicious upgrade could redirect depositor funds"
  - risk_id: oracle_staleness
    deployment: ethereum
    note: "Points and yield accrual in multi-layer LRT strategies depend on off-chain tracking of restaking points, which has no on-chain oracle; mismatch between advertised and realized yield can only be detected after distribution events"
audits: []
---

## Overview

Multipli.fi is a yield aggregator focused on leveraged points farming, primarily built
on top of LRT (Liquid Restaking Token) protocols and EigenLayer. Depositors supply ETH
or LRT assets; Multipli deploys capital to maximize restaking point accrual across multiple
protocols simultaneously. The protocol's TVL is structurally tied to EigenLayer's points
program and downstream LRT airdrop campaigns, making it a mercenary-capital vehicle rather
than a protocol with durable yield mechanics.

## Type-specific risks

See `types/yield_aggregator.md` for base risk profile.
