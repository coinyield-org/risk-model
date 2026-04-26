---
id: rwa
name: Real World Asset Protocol
description: On-chain representation of off-chain financial assets (bonds, credit, RE).
examples: [ondo_finance, centrifuge, maple_finance, goldfinch, backed_fi, openeden]
key_risks:
  - rwa_issuer_default
  - rwa_counterparty_default
  - oracle_coverage_absence
  - rwa_business_hours
  - kyc_bottleneck
  - issuer_corporate_risk
  - attestation_vs_audit_gap
  - fiat_ramp_gating
  - custodian_risk
  - blacklist_function
  - transfer_restriction_list
key_parameters:
  - nav_update_frequency
  - redemption_notice_period
  - minimum_investment
  - kyc_jurisdiction_restrictions
  - underlying_asset_duration
  - credit_rating_of_underlying
key_invariants:
  - "on_chain_supply * share_price <= off_chain_nav  (no overissuance)"
  - "redemption_available >= claimed_redemption_requests"
  - "underlying_assets audited or attested on schedule"
attack_patterns: []
---

## Mechanism

Protocol tokenizes off-chain assets (US Treasuries, credit pools, invoices).
On-chain token represents claim on off-chain NAV. Price updated periodically
by trusted oracle (often issuer itself). Redemption requires off-chain
settlement process.

## Type-specific risk profile

### Off-chain = opaque risk
Unlike fully on-chain DeFi, RWA risk is not fully observable on-chain:
- Underlying asset quality requires trust in issuer/attestor
- Redemption requires functional banking infrastructure
- NAV updates are discretionary (issuer controls timing)

This is the opposite of trustless DeFi — trust in specific legal entities
is explicitly required.

### NAV staleness is structural
NAV updates daily at best (bond markets close). Crypto markets run 24/7.
During market stress, RWA token may trade at substantial discount to
last reported NAV — arb is impossible because redemption is slow.
Lending protocols accepting RWA as collateral should use market price,
not NAV (same duality as LST exchange rate vs market price).

### Redemption gating
Minimum investment (typically $100K+), institutional KYC, business hours.
Retail cannot directly arb pricing discrepancies. Only large institutional
players can redeem → price discovery is slow and coarse.

### Counterparty concentration
ONDO (USDY) → holds US Treasuries via Ankura Trust + HSBC.
BUIDL (BlackRock) → BlackRock + BNY Mellon custodian.
All off-chain counterparties are regulated entities — their operational
status (business hours, holidays, legal proceedings) directly affects
on-chain token redemption.

### Regulatory trigger (operational, not regulatory risk)
Regulatory action against issuer entity (not the regulation itself) can
freeze token operations: issuer halts new mints, redemptions queued indefinitely.
This is operational risk via institutional counterparty, not regulatory.
