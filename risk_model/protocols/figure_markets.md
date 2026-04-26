---
slug: figure_markets
name: Figure Markets Exchange
types: [lending]
deployments:
  - chain: provenance
    tvl_usd: 1700000000
    since: 2021-01-01
    note: "Provenance Blockchain is Figure's proprietary Layer-1; non-EVM, not publicly audited via standard DeFi audit firms"
dependencies:
  - id: provenance_blockchain
    type: chain_validators
    scope: all_deployments
    note: "Figure controls the majority of Provenance validator set; chain liveness and censorship resistance depend on Figure Technologies Inc"
  - id: figure_technologies
    type: issuer
    scope: all_deployments
    note: "Figure Technologies Inc is the single issuer and operator; all loan origination, custody, and settlement flows through Figure entities"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: provenance
    note: "Figure Technologies Inc is the sole counterparty for loan origination and platform operation; corporate distress, regulatory action, or insolvency would impair all outstanding positions with no decentralized fallback"
  - risk_id: fallback_oracle_misconfig
    deployment: provenance
    note: "Provenance is a proprietary chain with no access to standard decentralized oracle networks (Chainlink, Pyth); price feeds for collateral assets depend on Figure-operated or custodian-provided data sources with no public deviation threshold or heartbeat SLA"
  - risk_id: deployer_key_leak
    deployment: provenance
    note: "Protocol upgrades and admin functions on Provenance are controlled by Figure-managed keys; the non-public validator and admin key infrastructure presents an unverifiable compromise surface"
  - risk_id: underlying_chain_dep
    deployment: provenance
    note: "Provenance is a permissioned chain controlled by Figure; liveness, censorship resistance, and finality are entirely dependent on Figure's infrastructure team — no decentralized fallback exists"
  - risk_id: per_deployment_divergence
    deployment: provenance
    note: "Non-EVM architecture means no standard tooling, no public Etherscan-equivalent explorer, and no audit trail compatible with DeFi-standard risk frameworks; risk assessment relies on Figure's proprietary disclosures"
audits: []
---

## Overview

Figure Markets Exchange is an OTC and institutional lending marketplace operating on
Provenance Blockchain, a proprietary Layer-1 built and primarily controlled by Figure
Technologies Inc. The platform facilitates collateralized lending (primarily HELOC and
crypto-backed loans) and secondary market trading of private credit assets. TVL is driven
by institutional and high-net-worth participants accessing private credit yield.

## Type-specific risks

See `types/lending.md` for base risk profile.

## Deployment divergence

Single-chain deployment on Provenance (non-EVM). The proprietary chain architecture means
standard DeFi risk tooling, oracle networks, and audit methodologies do not apply directly.
Risk assessment requires reliance on Figure's proprietary disclosures and off-chain legal
frameworks rather than on-chain verifiable parameters.
