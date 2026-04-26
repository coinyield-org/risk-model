---
slug: unit_bridge
name: Unit Bridge
types: [bridge]
deployments:
  - chain: ethereum
    tvl_usd: 440000000
    since: 2024-01-01
dependencies:
  - id: unit_team
    type: operator
    scope: all_deployments
    note: new protocol; team controls bridge ops
active_risks:
  - risk_id: bridged_backing_loss
    note: "Locked assets on source chain are the sole backing; bridge exploit or custodian failure = total loss"
  - risk_id: deployer_key_leak
    note: "New protocol with no documented multisig or timelock — upgrade EOA compromise is critical surface"
  - risk_id: guardian_key_leak
    note: "Guardian/pause key is a single point of failure with no publicly documented threshold structure"
  - risk_id: fallback_oracle_misconfig
    note: "No established oracle coverage documented for Unit Bridge; price feed absence creates liquidation blind spots"
audits: []
---

## Overview

Unit Bridge is a newly launched bridge protocol with ~$0.44B TVL. Little public
information exists on the operator structure, signing scheme, or security model.
The bridge appears to be operated by the Unit team with limited external validation.
No audit PDFs have been indexed; the protocol has not yet established the track
record or documented security practices of more mature bridges.

## Type-specific risks

See `types/bridge.md` for base risk profile.
