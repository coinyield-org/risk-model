---
slug: paxos_gold
name: Paxos Gold (PAXG)
types: [rwa]
deployments:
  - chain: ethereum
    tvl_usd: 2300000000
    since: 2019-09-26
dependencies:
  - id: paxos_trust_company
    type: issuer_custodian
    scope: all_deployments
    note: "Paxos Trust Company (NYDFS-regulated) issues PAXG and holds the backing gold; single custodian and single issuer"
  - id: brinks
    type: vault_operator
    scope: all_deployments
    note: "Physical gold is stored in Brinks vaults in London; operational vault custody is outsourced"
  - id: nydfs
    type: regulator
    scope: all_deployments
    note: "Paxos operates under NYDFS charter; regulatory action can affect issuance, redemption, or operations"
active_risks:
  - risk_id: rwa_issuer_default
    deployment: ethereum
    note: "Paxos Trust Company is the sole issuer and custodian of gold backing PAXG. Insolvency, regulatory revocation of Paxos's NYDFS charter, or operational failure would halt redemptions and potentially impair backing."
  - risk_id: custodian_risk
    deployment: ethereum
    note: "Physical gold is held by Paxos at Brinks vaults in London. Vault theft, natural disaster, or Brinks operational failure could impair the physical backing, though Paxos maintains insurance."
  - risk_id: rwa_business_hours
    deployment: ethereum
    note: "Physical gold redemption requires business-hours coordination with Paxos; on-chain PAXG transfers are 24/7 but cash redemption is limited to banking hours. Physical gold delivery adds further logistical delay."
  - risk_id: issuer_blacklist_function
    deployment: ethereum
    note: "Paxos retains the ability to freeze and seize PAXG token balances via a setLawEnforcementRole function. This has been exercised historically at the request of law enforcement."
  - risk_id: transfer_restriction_list
    deployment: ethereum
    note: "Paxos can restrict token transfers on a per-address basis in response to regulatory or legal requirements, creating counterparty risk for DeFi protocols that hold PAXG."
  - risk_id: attestation_vs_audit_gap
    deployment: ethereum
    note: "Gold backing is verified via monthly attestations by an independent firm, not continuous on-chain proof of reserves. The attestation window creates a gap during which backing discrepancies cannot be detected on-chain."
audits: []
---

## Overview

Paxos Gold (PAXG) is a gold-backed token issued by Paxos Trust Company, a
NYDFS-regulated US trust company. Each PAXG token represents one troy ounce of
physical gold held in Brinks vaults in London. Paxos publishes monthly reserve
attestations. PAXG is redeemable for physical gold or USD at the prevailing gold
spot price, subject to Paxos KYC requirements and business-hours availability.
Paxos retains freeze and seizure authority over token balances by design.

## Type-specific risks

See `types/rwa.md` for base risk profile.
