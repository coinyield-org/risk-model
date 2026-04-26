---
id: nft_lending
name: NFT Lending Protocol
description: Lending with NFTs or non-fungible positions (e.g., UniV3 LP) as collateral.
examples: [nftfi, paraspace, blur_blend, arcade_xyz, jpegd, metastreet]
key_risks:
  - oracle_coverage_absence
  - illiquid_collateral_liquidation
  - liquidation_bonus_too_small
  - thin_liquidity_source_manipulation
  - lp_position_single_sided_trap
  - concentrated_pool_dependency
  - whale_concentration
key_parameters:
  - floor_price_oracle_method
  - loan_to_floor_value_ratio
  - liquidation_auction_window
  - max_loan_duration
key_invariants:
  - "loan_amount <= nft_floor_price * ltv"
  - "liquidation completes within auction_window  (else bad debt)"
  - "oracle_price = recent_sale or floor  (not self-reported NAV)"
attack_patterns:
  - lp_position_single_sided_trap
---

## Mechanism

Borrower locks NFT as collateral → receives loan in ETH/stablecoin.
Liquidation triggered when loan_value > nft_value * threshold.
Liquidation = auction or peer-to-peer settlement (varies by protocol).

## Type-specific risk profile

### NFT liquidity is fundamentally different from fungible assets
- No order book depth: NFT liquidity = recent sales in small numbers
- Floor price oracle = lagging, manipulable (wash trading)
- Liquidation auction requires real buyer at distressed moment

### Wash trading attacks floor price oracle
Floor price = minimum recent sale price. Attacker self-trades NFTs
to inflate floor → borrows excess against inflated collateral → defaults.
Wash trading is cheap if attacker values manipulation > liquidation profit.

### UniV3 LP position as NFT collateral
Concentrated LP position value depends on:
- Current price vs tick range
- Range status (in/out of range)
- Fee accrual rate

Price move pushing LP out of range = position becomes 100% single-asset
AND earns no fees. Value collapses by more than underlying price change.
Requires real-time dynamic valuation, not static floor oracle.

### Liquidation auction is slow
Unlike fungible liquidation (instant swap), NFT auction takes hours to days.
During auction, floor price may continue falling → winner pays more than
market → no bidders → bad debt.
