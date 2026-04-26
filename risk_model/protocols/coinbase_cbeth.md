---
slug: coinbase_cbeth
name: Coinbase cbETH
types: [lst]
deployments:
  - chain: ethereum
    tvl_usd: 240000000
    since: 2022-08-11
  - chain: base
    tvl_usd: 50000000
    since: 2023-08-01
    note: "cbETH on Base is bridged from Ethereum via the native Base bridge"
  - chain: optimism
    tvl_usd: 20000000
    since: 2023-06-01
    note: "cbETH on Optimism is bridged from Ethereum via the native OP bridge"
dependencies:
  - id: coinbase_exchange
    type: node_operator
    scope: [ethereum]
    note: "Coinbase runs 100% of the validators backing cbETH; there is no decentralized operator set — all staking is performed by Coinbase's institutional infrastructure"
  - id: ethereum_beacon_chain
    type: underlying_chain
    scope: [ethereum]
    note: "Validator rewards and penalties are determined by Ethereum consensus rules; Coinbase validators are subject to the same slashing conditions as all validators"
  - id: coinbase_institutional
    type: custodian
    scope: [ethereum]
    note: "Coinbase institutional trust framework governs cbETH issuance; the cbETH token contract includes admin controls managed by Coinbase"
active_risks:
  - risk_id: operator_concentration
    deployment: ethereum
    note: "Coinbase runs all cbETH validators through its own infrastructure; a Coinbase operational failure, regulatory forced-exit (SEC enforcement, bank partnership loss), or coordinated slashing event would affect 100% of cbETH backing simultaneously — there is no operator diversification as in Lido or Rocket Pool"
  - risk_id: issuer_corporate_risk
    deployment: ethereum
    note: "Coinbase has been subject to significant SEC enforcement proceedings; a forced operational shutdown, asset freeze order, or loss of banking relationships at Coinbase would impair cbETH redeemability and could trigger a forced mass validator exit that exceeds Ethereum's exit queue capacity"
  - risk_id: exchange_rate_vs_market_depeg
    deployment: [ethereum, base, optimism]
    note: "cbETH market price can deviate from its ETH exchange rate during periods of market stress or forced selling; Coinbase's regulatory situation has historically triggered cbETH discount periods — the peg relies on Coinbase's ability and willingness to honor redemptions"
  - risk_id: issuer_blacklist_function
    deployment: [ethereum, base, optimism]
    note: "The cbETH token contract includes a blacklisting function controlled by Coinbase; Coinbase can freeze individual cbETH balances in response to regulatory orders, law enforcement requests, or internal compliance decisions — making cbETH non-neutral as a DeFi collateral asset"
  - risk_id: deployer_key_leak
    deployment: ethereum
    note: "No public smart contract audit PDFs have been identified for cbETH; the cbETH contract upgrade authority and admin controls are held by Coinbase, whose key management practices have not been independently verified in a published audit"
audits: []
---

## Overview

Coinbase cbETH is a liquid staking token representing ETH staked through Coinbase's
institutional validator infrastructure. Unlike Lido or Rocket Pool, cbETH has no
decentralized operator set — Coinbase runs all backing validators, making it the most
centralized major LST by operator structure. cbETH includes a blacklisting function
that allows Coinbase to freeze balances, reflecting compliance requirements that
distinguish it from censorship-resistant LSTs. Coinbase's ongoing regulatory exposure
(SEC enforcement proceedings) is the dominant exogenous risk factor.

## Type-specific risks

See `types/lst.md` for base risk profile.

## Deployment divergence

cbETH on Base and Optimism is bridged from Ethereum via native bridges. Bridge latency
means the L2 exchange rate can lag behind Ethereum during rapid market moves. Withdrawals
from L2 back to Ethereum are subject to the native bridge's finality delay (7 days for
Optimism, shorter for Base post-Fault Proofs). No independent staking occurs on L2.

## Key parameters (ethereum, as of 2026-01)

| Parameter | Value |
|-----------|-------|
| Operator set | Coinbase (sole operator) |
| Blacklist function | Yes — Coinbase-controlled |
| Withdrawal model | Coinbase-managed; redemption at exchange rate |
| Regulatory exposure | SEC enforcement history; ongoing proceedings |
| Audit coverage | None in indexed PDFs |
