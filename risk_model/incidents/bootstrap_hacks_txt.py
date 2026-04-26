"""
bootstrap_hacks_txt.py

Parses a plain-text list of DefiLlama hack entries (hacks.txt) and generates
auto_*.yaml incident stubs for DeFi-on-chain scope only.

Input format per line:
    N. Name | Date (DD Mon, YYYY) | Amount ($X | $Xk | $Xm | $Xb) | URL

Excluded (out of scope):
  - Centralised exchange / hot-wallet hacks
  - Wallet / drainer / frontend-tool incidents
  - Social-media-only / non-crypto events

Promoted (manual override):
  KNOWN_INCIDENTS — a curated list of well-known incidents where the
  event_type, risk_ids, and confidence are pre-filled. First match wins.

Entries not matched by KNOWN_INCIDENTS are classified by keyword rules on the
incident name. Unclassified entries are written with empty risk_ids and a
note asking for manual review.

Usage (from repo root):
    python coinyield-data/risk_model/incidents/bootstrap_hacks_txt.py \\
        --input path/to/hacks.txt
"""

import argparse
import os
import re
import sys

# Shared helpers from the DeFiHackLabs bootstrapper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bootstrap_defillama import (  # noqa: E402
    infer_chain_from_url,
    match_protocol_slugs,
    slugify,
    write_yaml,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MIN_AMOUNT_USD = 10_000  # skip tiny / near-miss events below this threshold

MONTH_MAP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}

# Case-insensitive substring match on the incident name.
# Uses word-boundary regex so short tokens like "rain" do not match "rainbow".
EXCLUDE_PATTERNS = [
    # --- Centralised exchanges / custodians ---
    "bybit", "ftx", "wazirx", "btcturk", "coindcx", "dmm bitcoin", "phemex",
    "nobitex", "bingx", "woo x", "bitget", "grinex", "xt exchange",
    "m2 exchange", "indodax", "coinspaid", "infini", "ascendex", "bitmart",
    "crypto.com", "lcx", "bitrue", "gdac", "coinex", "huobi", "htx",
    "poloniex", "coinspot", "alphapo", "remitano", "stake.com", "fixedfloat",
    "deribit", "duelbits", "kraken", "cryptocom",
    # Hedera -- keep (L1 ecosystem)
    # HTX / Huobi -- excluded as CEX
    # --- Wallets / drainer tools / trading bots ---
    "zerion wallet", "myalgo", "rabby wallet", "bitkeep", "banana gun",
    "dexx", "coinstats", "dogwiftools", "moonhacker", "slope wallet",
    "atomic wallet", "maestro", "unibot", "profanity ethereum vanity",
    # --- Social / frontend / unrelated ---
    "hacked twitters", "btc etf", "us government crypto wallet",
    "okx nft aggregator", "geniusai",
    # Rain is a corporate card issuer, not a DeFi protocol
    "rain",
]

_EXCLUDE_REGEXES = [
    re.compile(rf"\b{re.escape(p)}\b")
    for p in EXCLUDE_PATTERNS
]


def is_excluded(name: str) -> bool:
    low = name.lower()
    return any(rx.search(low) for rx in _EXCLUDE_REGEXES)


# First match wins. Pattern tested against name + url (lowercased, joined with space).
CLASSIFICATION_RULES = [
    (
        r"\bbridge\b|cross[- ]?chain|\bxbridge\b|\bforcebridge\b|\bhyperbridge\b",
        "bridge",
        ["bridge_dep", "bridge_signing_committee"],
    ),
    (
        r"\boracle\b|\btwap\b|price\s+manipulation|price\s+oracle",
        "oracle_failure",
        ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
    ),
    (
        r"\bgovernance\b|\bproposal\b|dao\s+takeover",
        "governance",
        ["flash_governance", "hostile_proposal_via_delegation"],
    ),
    (
        r"rug[\s-]pull|\brug\b|exit\s+scam",
        "governance",
        ["governance_hostile_decision", "deployer_key_leak"],
    ),
    (
        r"private\s+key|signer\s+compromise|multisig\s+compromise",
        "exploit",
        ["governance_signer_key_leak", "deployer_key_leak"],
    ),
    (
        r"depeg|algo(rithmic)?\s+stable|death\s+spiral",
        "depeg",
        ["stablecoin_depeg", "soft_peg_algo_failure"],
    ),
    (
        r"bad\s+debt",
        "bad_debt",
        ["bad_debt_socialization", "insurance_fund_depletion"],
    ),
]

_CLASSIFIERS = [
    (re.compile(pat, re.IGNORECASE), event_type, risk_ids)
    for pat, event_type, risk_ids in CLASSIFICATION_RULES
]


def classify_by_keywords(name: str, url: str) -> tuple[str | None, list[str]]:
    blob = f"{name} {url}".lower()
    for rx, event_type, risk_ids in _CLASSIFIERS:
        if rx.search(blob):
            return event_type, list(risk_ids)
    return None, []


# ---------------------------------------------------------------------------
# Manually curated high/medium-confidence mappings.
# First entry with (date exact match) and (name_contains substring match) wins.
# ---------------------------------------------------------------------------

KNOWN_INCIDENTS = [
    # ------------------ Bridges (bridge_dep / bridge_signing_committee) ------------------
    {
        "date": "2021-08-10", "name_contains": "poly network",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee", "governance_signer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Poly Network (Aug 2021): attacker called a privileged relay keeper "
            "function to replace the authorized keeper address with their own, then "
            "withdrew assets across Ethereum/BSC/Polygon. ~$611M stolen, later fully "
            "returned. Key admin function with no timelock."
        ),
    },
    {
        "date": "2022-03-23", "name_contains": "ronin",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee", "validator_key_share_compromise"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Lazarus Group compromised 5 of 9 Ronin Bridge validator signing keys "
            "(including four held by Sky Mavis and one delegated by Axie DAO) and "
            "forged two withdrawal transactions draining 173,600 ETH + 25.5M USDC. "
            "Canonical example of bridge-signing-committee key compromise."
        ),
    },
    {
        "date": "2024-08-06", "name_contains": "ronin bridge",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Second Ronin Bridge incident: a whitehat MEV bot front-ran an "
            "exploit triggered by a faulty upgrade; funds were returned. "
            "Evidence of per-deployment bridge-upgrade risk."
        ),
    },
    {
        "date": "2022-10-06", "name_contains": "bnb bridge",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "BSC Token Hub / Binance Bridge: IAVL Merkle-proof verification flaw "
            "allowed forging cross-chain withdrawal messages and minting 2M BNB "
            "(~$570M). Bridge-dep / cross-chain message-verification failure."
        ),
    },
    {
        "date": "2022-10-06", "name_contains": "binance bridge",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "Alias for BNB Bridge: IAVL Merkle-proof forgery exploit, ~$570M "
            "minted on BSC before chain was halted."
        ),
    },
    {
        "date": "2022-02-02", "name_contains": "portal",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "high",
        "affected_protocols": ["portal_wormhole"],
        "chains": ["solana", "ethereum"],
        "notes": (
            "Portal / Wormhole bridge signature verification bypass on the "
            "Solana side allowed minting 120,000 wETH (~$326M) without locking "
            "ETH on Ethereum. Classic bridge-dep backing-loss."
        ),
    },
    {
        "date": "2022-08-01", "name_contains": "nomad",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Nomad bridge: root of the Merkle tree was initialised to 0x00 in a "
            "routine upgrade, making every pre-signed message replayable. "
            "Free-for-all drain of ~$190M. Bridge message-verification failure."
        ),
    },
    {
        "date": "2022-06-23", "name_contains": "harmony",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Harmony Horizon bridge: 2-of-5 multisig compromise (private keys "
            "of two signers were stolen). Attacker drained ~$100M. "
            "Textbook bridge-signing-committee risk."
        ),
    },
    {
        "date": "2023-07-07", "name_contains": "multichain",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee", "governance_signer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Multichain: CEO held all MPC signing keys and was arrested in "
            "China; funds on multiple bridged deposits were unilaterally moved. "
            "~$126M lost. Key-operator concentration plus opaque MPC signing."
        ),
    },
    {
        "date": "2023-11-22", "name_contains": "heco",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee", "governance_signer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "HECO bridge + HTX drain via signer key compromise (~$86.6M). "
            "Attributed to the same operator (Justin Sun) holding both sets "
            "of keys."
        ),
    },
    {
        "date": "2023-12-31", "name_contains": "orbit bridge",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Orbit Bridge: 7 of 10 validator signatures forged via compromised "
            "keys / suspicious validator concentration. ~$81.7M lost across "
            "USDT / USDC / ETH / WBTC / DAI."
        ),
    },
    {
        "date": "2022-06-08", "name_contains": "optimism bridge",
        "event_type": "bridge",
        "risk_ids": ["bridge_dep"],
        "confidence": "medium",
        "affected_protocols": ["optimism_bridge"],
        "chains": ["ethereum", "optimism"],
        "notes": (
            "Wintermute / Optimism: 20M OP tokens sent to an unrecoverable "
            "Gnosis Safe address during an OP bridge multisig handoff. "
            "Operational process failure during bridge deployment."
        ),
    },
    {
        "date": "2023-07-02", "name_contains": "poly network",
        "event_type": "bridge",
        "risk_ids": ["bridge_signing_committee"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Second Poly Network incident (2023): keepers compromised, "
            "allowing attacker to mint bridged assets on multiple destination "
            "chains (~$5M usable)."
        ),
    },

    # ------------------ Oracle / price manipulation ------------------
    {
        "date": "2020-10-26", "name_contains": "harvest",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Harvest Finance: attacker flash-loaned $50M USDC and $17M USDT to "
            "manipulate Curve's y-pool, temporarily depressing USDC/USDT price in "
            "the pool oracle. Harvest vaults used this price to calculate share "
            "value, allowing cheap withdrawals. ~$33.8M."
        ),
    },
    {
        "date": "2021-02-13", "name_contains": "alpha",
        "event_type": "bad_debt",
        "risk_ids": ["bad_debt_accumulation", "thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Alpha Homora / Iron Bank: attacker exploited a logic flaw to take flash "
            "loans without repaying, creating $37.5M of bad debt in Iron Bank "
            "(Cream v2). The Iron Bank had no circuit breaker for unlimited borrowing."
        ),
    },
    {
        "date": "2021-05-12", "name_contains": "xtoken",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "xToken: attacker flash-loaned to manipulate the xSNXa AMM price used "
            "as collateral oracle, then borrowed all protocol assets. ~$24.5M lost. "
            "Thin-liquidity oracle source on shallow xToken pools."
        ),
    },
    {
        "date": "2021-05-20", "name_contains": "pancakebunny",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "PancakeBunny: attacker used flash loan to manipulate BUNNY price in "
            "thin BNB/BUNNY pool (used as mint oracle), causing massive BUNNY minting "
            "and immediate dump. ~$45M lost. Thin-liquidity oracle on own token pool."
        ),
    },
    {
        "date": "2021-05-29", "name_contains": "belt finance",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "Belt Finance (BSC): flash loan price manipulation in Ellipsis pool used "
            "as 4Belt share price oracle. Attacker cycled funds to manipulate price "
            "and extract yield. ~$6.2M. Oracle from manipulable pool."
        ),
    },
    {
        "date": "2022-04-28", "name_contains": "deus",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "DEUS Finance: attacker used flash loan to manipulate the USDC/DEI "
            "Solidly AMM pool price, which served as the oracle for DEI collateral. "
            "~$13.4M. Thin-liquidity oracle manipulation on AMM."
        ),
    },
    {
        "date": "2022-04-30", "name_contains": "saddle",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Saddle Finance: attacker manipulated the virtual price of the "
            "saddleUSD-V2 metapool to drain ~$11M. Price manipulation via flash loan "
            "on thin Saddle liquidity."
        ),
    },
    {
        "date": "2022-11-06", "name_contains": "pando",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "Pando Rings (Mixin-based lending): price oracle manipulation exploited "
            "the thin on-chain liquidity for MOB and pUSD collateral assets. ~$22M. "
            "Thin-liquidity oracle on small-cap collateral."
        ),
    },
    {
        "date": "2022-11-10", "name_contains": "dfx finance",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "DFX Finance: attacker used flash loan + reentrancy on the AMM curve to "
            "manipulate virtual price and extract funds. ~$7.5M. Oracle/price-curve "
            "manipulation via reentrancy-enabled flash loan."
        ),
    },
    {
        "date": "2022-10-11", "name_contains": "mango markets",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["solana"],
        "notes": (
            "Avraham Eisenberg pumped MNGO-PERP price on the illiquid Mango "
            "oracle source, marked his own long to ~$116M unrealised PnL, and "
            "borrowed the treasury against it. Canonical example of thin-"
            "liquidity oracle manipulation against an on-book mark-price."
        ),
    },
    {
        "date": "2024-06-10", "name_contains": "uwu lend",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "UwU Lend (Sifu): sUSDe oracle pulled price from Curve pools with "
            "shallow liquidity; flash-loan-funded swaps moved the oracle and "
            "allowed borrowing against overvalued collateral. ~$20M drained."
        ),
    },
    {
        "date": "2024-06-13", "name_contains": "uwu lend",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "UwU Lend second exploit three days after the $20M attack: same "
            "oracle-manipulation primitive reapplied before the protocol was "
            "fully paused."
        ),
    },
    {
        "date": "2024-11-16", "name_contains": "polter",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "Polter Finance (Fantom Aave v2 fork): BOO token oracle price "
            "manipulated via thin-liquidity pool; attacker borrowed the "
            "protocol against inflated collateral. ~$12M drained."
        ),
    },
    {
        "date": "2023-02-01", "name_contains": "bonq",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["polygon"],
        "notes": (
            "BonqDAO used Tellor push-price oracle with no deviation bounds. "
            "Attacker updated WALBT price up and down to mint BEUR and drain "
            "collateral. ~$88M notional (mostly illiquid WALBT)."
        ),
    },
    {
        "date": "2022-04-02", "name_contains": "inverse",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Inverse Finance: Keep3r TWAP oracle for INV was pulled from a "
            "low-liquidity SushiSwap pool. Attacker pumped the pool, borrowed "
            "against inflated INV, repaid nothing. ~$15.6M lost."
        ),
    },
    {
        "date": "2021-10-27", "name_contains": "cream",
        "event_type": "oracle_failure",
        "risk_ids": ["thin_liquidity_source_manipulation", "bad_debt_accumulation"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Cream Finance v1 (Oct 2021): attacker manipulated yUSDVault share "
            "price used as collateral oracle, borrowed ~$130M against fake "
            "collateral. Oracle-dependent on-chain share-price inflation."
        ),
    },

    # ------------------ Governance attacks ------------------
    {
        "date": "2021-03-04", "name_contains": "meerkat",
        "event_type": "governance",
        "risk_ids": ["deployer_key_leak", "governance_hostile_decision"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "Meerkat Finance (BSC): one day after launch, team exploited "
            "upgradeability to drain all user deposits (~$31M). Claimed it was a "
            "'test' but returned nothing. Classic deployer-controlled upgrade rug."
        ),
    },
    {
        "date": "2022-04-17", "name_contains": "beanstalk",
        "event_type": "governance",
        "risk_ids": ["flash_governance"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Beanstalk: attacker flash-loaned $1B in stables/BEAN to buy >66% "
            "of Stalk voting power, passed two 'emergency' proposals that "
            "transferred $181M to their address. No proposal timelock. "
            "Canonical flash-governance exploit."
        ),
    },
    {
        "date": "2023-05-20", "name_contains": "tornado cash",
        "event_type": "governance",
        "risk_ids": ["hostile_proposal_via_delegation", "governance_hostile_decision"],
        "confidence": "high",
        "affected_protocols": ["tornado_cash"],
        "chains": ["ethereum"],
        "notes": (
            "Tornado Cash governance takeover: attacker deployed a malicious "
            "proposal router that passed a benign-looking vote and then "
            "upgraded governance to hand over 100% of voting power. No funds "
            "lost after whitehat coordination, but demonstrated governance "
            "capture via delegation."
        ),
    },
    {
        "date": "2021-11-05", "name_contains": "ooki",
        "event_type": "governance",
        "risk_ids": ["governance_hostile_decision"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "bZx / Ooki DAO: pre-existing insolvent position inherited by DAO "
            "after migrating to on-chain governance; CFTC later held DAO "
            "voters jointly liable. Evidence of DAO-as-legal-person risk."
        ),
    },

    # ------------------ Rug pulls / deployer-key / exit scams ------------------
    {
        "date": "2024-03-26", "name_contains": "munchables",
        "event_type": "governance",
        "risk_ids": ["deployer_key_leak", "insider_asymmetry"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "Munchables (Blast L2): rogue North Korean developer inserted a "
            "backdoor into upgradeable contracts during development, drained "
            "$62.5M on launch. Funds recovered after identification. "
            "Classic insider-backdoor / deployer-key risk."
        ),
    },
    {
        "date": "2021-10-29", "name_contains": "anubis",
        "event_type": "governance",
        "risk_ids": ["deployer_key_leak", "governance_hostile_decision"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "AnubisDAO: LP tokens from launch were sent to an EOA controlled "
            "by one anonymous dev; ~$60M drained within 20 hours of launch. "
            "Deployer-key / undisclosed-admin risk."
        ),
    },
    {
        "date": "2022-12-24", "name_contains": "defrost",
        "event_type": "governance",
        "risk_ids": ["deployer_key_leak", "governance_hostile_decision"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["avalanche"],
        "notes": (
            "Defrost Finance v2: deployer added a malicious oracle and "
            "liquidated all positions into their own address. Rug via hidden "
            "admin authority. ~$12M drained."
        ),
    },

    # ------------------ Signer / key / multisig compromise ------------------
    {
        "date": "2022-12-02", "name_contains": "ankr",
        "event_type": "exploit",
        "risk_ids": ["deployer_key_leak", "unauthorized_mint"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["bnb"],
        "notes": (
            "Ankr: compromised deployer key allowed minting ~6 quadrillion aBNBc "
            "tokens, which were then sold on DEXs. ~$5M direct loss plus ~$15M "
            "downstream contagion to HAY stablecoin that used aBNBc as collateral."
        ),
    },
    {
        "date": "2023-05-05", "name_contains": "deus dao v3",
        "event_type": "exploit",
        "risk_ids": ["governance_signer_key_leak", "deployer_key_leak"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["arbitrum"],
        "notes": (
            "DEUS Finance (v3, May 2023): deployer/admin key compromised allowing "
            "minting of DEI stablecoin and draining of protocol reserves. ~$6.5M. "
            "Admin-key / minter-authority single point of failure."
        ),
    },
    {
        "date": "2023-08-07", "name_contains": "steadefi",
        "event_type": "exploit",
        "risk_ids": ["deployer_key_leak", "governance_signer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["arbitrum", "avalanche"],
        "notes": (
            "Steadefi: deployer's private key was phished/stolen; attacker upgraded "
            "proxy contracts to drain all user vaults. ~$1.1M. Admin-key loss "
            "enabling proxy upgrade attack."
        ),
    },
    {
        "date": "2024-05-14", "name_contains": "alex",
        "event_type": "exploit",
        "risk_ids": ["deployer_key_leak", "insider_asymmetry"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "Alex Protocol (Stacks/Bitcoin L2): rogue developer (later linked to "
            "North Korea) embedded a backdoor in the upgradeable contract, draining "
            "~$4M in stablecoins. Similar pattern to Munchables (Blast). Insider "
            "deployer-key risk."
        ),
    },
    {
        "date": "2022-09-20", "name_contains": "wintermute",
        "event_type": "exploit",
        "risk_ids": ["deployer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "Wintermute hot-wallet drained via Profanity-generated vanity "
            "address with brute-forceable private key. ~$160M lost. "
            "Evidence that operational key-generation tooling can be the "
            "single point of failure even for sophisticated operators."
        ),
    },
    {
        "date": "2024-10-16", "name_contains": "radiant",
        "event_type": "exploit",
        "risk_ids": ["governance_signer_key_leak", "deployer_key_leak"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["arbitrum", "bnb"],
        "notes": (
            "Radiant V2: 3 of 11 multisig signers compromised via malware on "
            "hardware-wallet-driver machines; signers approved what they "
            "believed was routine ownership transfer but was an upgrade to "
            "malicious implementation. ~$53M drained across Arbitrum + BSC."
        ),
    },
    {
        "date": "2021-12-02", "name_contains": "badger",
        "event_type": "exploit",
        "risk_ids": ["frontend_js_injection", "wallet_supply_chain"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "BadgerDAO: malicious Cloudflare API key injected JavaScript into "
            "the frontend that prompted users to sign unlimited-approval "
            "transactions. ~$120M drained. Frontend / off-chain supply-chain "
            "attack, not a contract bug."
        ),
    },

    # ------------------ Stablecoin depeg (collateral_asset) ------------------
    {
        "date": "2021-06-16", "name_contains": "iron finance",
        "event_type": "depeg",
        "risk_ids": ["soft_peg_algo_failure", "death_spiral", "self_fulfilling_depeg"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["polygon"],
        "notes": (
            "Iron Finance algorithmic stablecoin IRON partially backed by TITAN. "
            "A large sell triggered a bank run that crashed TITAN to near-zero, "
            "breaking the redemption peg in a textbook death spiral. First major "
            "algorithmic stablecoin collapse."
        ),
    },
    {
        "date": "2022-05-09", "name_contains": "terra",
        "event_type": "depeg",
        "risk_ids": ["soft_peg_algo_failure", "death_spiral", "self_fulfilling_depeg", "depeg_feedback_loop"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": [],
        "notes": (
            "Terra UST algorithmic stablecoin collapse: large UST sells drained "
            "Curve pool, triggered the mint-burn arbitrage loop that hyperinflated "
            "LUNA supply. UST lost peg permanently. ~$40B market cap destroyed. "
            "Canonical algorithmic stablecoin death spiral."
        ),
    },
    {
        "date": "2022-06-13", "name_contains": "steth",
        "event_type": "depeg",
        "risk_ids": ["lst_lrt_depeg", "contagion_bank_run", "systemic_reflexivity"],
        "confidence": "high",
        "affected_protocols": ["lido"],
        "chains": ["ethereum"],
        "notes": (
            "Celsius Network and Three Arrows Capital forced large stETH sales to "
            "meet redemptions. stETH depegged to ~0.94 ETH due to the withdrawal "
            "queue preventing arbitrage. First major LST depeg event, evidencing "
            "systemic reflexivity between CeFi leverage and LST liquidity."
        ),
    },
    {
        "date": "2023-03-10", "name_contains": "usdc",
        "event_type": "depeg",
        "risk_ids": ["stablecoin_depeg", "contagion_bank_run"],
        "confidence": "high",
        "affected_protocols": [],
        "chains": ["ethereum"],
        "notes": (
            "USDC briefly depegged to ~$0.87 after Circle revealed $3.3B in "
            "reserves held at Silicon Valley Bank (SVB) which failed on March 10. "
            "Triggered cascading bank runs across DeFi protocols using USDC as "
            "collateral."
        ),
    },
    # Terra UST collapse also exists as 2022-05-09_terra_ust_collapse.yaml;
    # the 2023-03-29 TerraUSD entry in hacks.txt is a court-order asset freeze
    # and is left to the keyword classifier.

    # ------------------ Bad debt / insurance fund ------------------
    {
        "date": "2023-04-15", "name_contains": "hundred finance",
        "event_type": "bad_debt",
        "risk_ids": ["bad_debt_accumulation"],
        "confidence": "medium",
        "affected_protocols": [],
        "chains": ["arbitrum"],
        "notes": (
            "Hundred Finance (Arbitrum): ERC4626 share inflation attack (donation "
            "to empty market) enabled minting hWBTC at favorable rate and draining "
            "collateral. ~$7.4M. Compound v2 fork inflation / bad-debt accumulation."
        ),
    },
    # Hyperliquid JELLY already exists; no other clean fits in hacks.txt.

    # ------------------ OOS marker: well-known pure code bugs ------------------
    # Per user direction, these still get stubs but with empty risk_ids.
    # Nothing to add here — default path handles them.
]


# ---------------------------------------------------------------------------
# Date / amount / line parsing
# ---------------------------------------------------------------------------

def parse_date(raw: str) -> str | None:
    """
    Parse 'DD Mon, YYYY' into 'YYYY-MM-DD'. Returns None on failure.
    """
    m = re.match(r"^\s*(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s*,\s*(\d{4})\s*$", raw)
    if not m:
        return None
    day, mon_abbr, year = m.group(1), m.group(2)[:3].title(), m.group(3)
    month = MONTH_MAP.get(mon_abbr)
    if not month:
        return None
    return f"{year}-{month}-{int(day):02d}"


def parse_amount(raw: str) -> int:
    """
    Parse amounts like $80,000 | $3.5m | $293m | $1.4b.
    Returns USD int. 0 on failure.
    """
    s = raw.strip().replace(",", "")
    m = re.match(r"^[~>]?\s*\$?([\d.]+)\s*([kKmMbB])?\s*$", s)
    if not m:
        return 0
    try:
        value = float(m.group(1))
    except ValueError:
        return 0
    suffix = (m.group(2) or "").lower()
    mult = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(suffix, 1)
    return int(value * mult)


_LINE_RE = re.compile(
    r"^\s*(\d+)\.\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([^|]+?)\s*(?:\|\s*(.*))?$"
)


def parse_line(line: str) -> dict | None:
    """
    Parse one line of hacks.txt. Returns a dict with keys:
        index, name, date_raw, amount_raw, url
    Returns None if the line is not a hack entry.
    """
    line = line.rstrip()
    if not line or line.startswith("**") or line.startswith("#") or line.startswith("---"):
        return None

    m = _LINE_RE.match(line)
    if not m:
        return None

    url_raw = (m.group(5) or "").strip()
    # Strip empty-URL markers: '—' (em dash), 'нет ссылки', '-', blank
    url_low = url_raw.lower()
    if url_raw in ("—", "-", "") or "нет ссылки" in url_low:
        url_raw = ""
    # Only accept real http(s) URLs
    if url_raw and not re.match(r"^https?://", url_raw):
        url_raw = ""

    return {
        "index": int(m.group(1)),
        "name": m.group(2).strip(),
        "date_raw": m.group(3).strip(),
        "amount_raw": m.group(4).strip(),
        "url": url_raw,
    }


def parse_hacks_txt(path: str) -> list[dict]:
    records = []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            rec = parse_line(raw)
            if not rec:
                continue
            date = parse_date(rec["date_raw"])
            if not date:
                continue
            amount = parse_amount(rec["amount_raw"])
            records.append({
                "index": rec["index"],
                "name": rec["name"],
                "date": date,
                "amount_usd": amount,
                "url": rec["url"],
            })
    return records


# ---------------------------------------------------------------------------
# Matching against KNOWN_INCIDENTS
# ---------------------------------------------------------------------------

def match_known(rec: dict) -> dict | None:
    name_low = rec["name"].lower()
    for entry in KNOWN_INCIDENTS:
        if entry["date"] != rec["date"]:
            continue
        if entry["name_contains"].lower() not in name_low:
            continue
        return entry
    return None


# ---------------------------------------------------------------------------
# Dedup against existing YAMLs in out_dir (exact filename + near-date match)
# ---------------------------------------------------------------------------

_DATE_IN_FILENAME = re.compile(r"(\d{4}-\d{2}-\d{2})_(.+)\.yaml$")


def existing_incidents(out_dir: str) -> list[tuple[str, str]]:
    """
    Return list of (date_str, slug_prefix) for all existing *.yaml files.
    Used for near-date dedup.
    """
    entries = []
    for fn in os.listdir(out_dir):
        if not fn.endswith(".yaml"):
            continue
        base = fn
        if base.startswith("auto_"):
            base = base[len("auto_"):]
        m = _DATE_IN_FILENAME.match(base)
        if not m:
            continue
        date = m.group(1)
        slug = m.group(2)
        entries.append((date, slug))
    return entries


def date_to_ordinal(date: str) -> int:
    y, m, d = date.split("-")
    return int(y) * 365 + int(m) * 31 + int(d)


def is_near_duplicate(date: str, slug: str, existing: list[tuple[str, str]]) -> bool:
    """
    True if an existing file has the same 10-char slug prefix and the dates are
    within 3 days of each other. Cheap approximation of same-incident matching.
    """
    ord_new = date_to_ordinal(date)
    prefix = slug[:10]
    for ed, es in existing:
        if abs(date_to_ordinal(ed) - ord_new) > 3:
            continue
        if prefix and es.startswith(prefix):
            return True
        if prefix and prefix in es[:12]:
            return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_stub(rec: dict) -> dict:
    """
    Build the incident dict for YAML output.
    """
    name = rec["name"]
    slug = slugify(name)
    date = rec["date"]
    incident_id = f"incident:{date}_{slug}"

    known = match_known(rec)

    if known:
        event_type = known["event_type"]
        risk_ids = list(known["risk_ids"])
        confidence = known["confidence"]
        # Respect explicit empty affected_protocols / chains in KNOWN_INCIDENTS.
        # Only fall back to name-based matching when the key is missing entirely.
        if "affected_protocols" in known:
            affected_protocols = list(known["affected_protocols"])
        else:
            affected_protocols = match_protocol_slugs(name)
        chains = list(known.get("chains", []))
        notes = known["notes"]
    else:
        event_type, risk_ids = classify_by_keywords(name, rec["url"])
        confidence = "low"
        affected_protocols = match_protocol_slugs(name)
        chains = []
        if rec["url"]:
            chain = infer_chain_from_url(rec["url"])
            if chain:
                chains.append(chain)
        if event_type is None:
            event_type = "exploit"
            notes = (
                f"Auto-generated from DefiLlama hacks list (hacks.txt entry #{rec['index']}). "
                "No taxonomy risk_id confidently fits from the name alone; "
                "manual review required. Leave risk_ids empty rather than guessing."
            )
        else:
            notes = (
                f"Auto-generated from DefiLlama hacks list (hacks.txt entry #{rec['index']}). "
                f"Classified by keyword match. Review and update confidence before use."
            )

    source_urls = [rec["url"]] if rec["url"] else []

    data = {
        "id": incident_id,
        "title": name,
        "date": date,
        "event_type": event_type,
        "amount_lost_usd": rec["amount_usd"],
        "near_miss": rec["amount_usd"] == 0,
        "affected_protocols": affected_protocols,
        "affected_assets": [],
        "chains": chains,
        "root_cause_entity": "",
        "cascade_targets": [],
        "risk_ids": risk_ids,
        "source_urls": source_urls,
        "confidence": confidence,
        "notes": notes,
    }
    return data


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate incident YAML stubs from a DefiLlama hacks.txt dump."
    )
    default_dir = os.path.dirname(os.path.abspath(__file__))
    default_candidates = [
        os.path.abspath(
            os.path.join(default_dir, "..", "..", "internal", "raw_inputs", "hacks", "hacks.txt")
        ),
        os.path.abspath(
            os.path.join(default_dir, "..", "..", "hacks.txt")
        ),
    ]
    default_input = next((path for path in default_candidates if os.path.exists(path)), default_candidates[0])
    parser.add_argument(
        "--input", default=default_input,
        help=f"Path to hacks.txt (default: {default_input}).",
    )
    parser.add_argument(
        "--out-dir", default=default_dir,
        help=f"Output directory (default: {default_dir}).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print counters and do not write files.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = os.path.abspath(args.out_dir)
    input_path = os.path.abspath(args.input)

    if not os.path.isfile(input_path):
        print(f"[error] Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(out_dir):
        print(f"[error] Output dir not found: {out_dir}", file=sys.stderr)
        sys.exit(1)

    records = parse_hacks_txt(input_path)
    print(f"Parsed {len(records)} entries from {input_path}")

    existing = existing_incidents(out_dir)
    print(f"Found {len(existing)} existing incident YAMLs in {out_dir}")

    stats = {
        "excluded": 0,
        "too_small": 0,
        "near_duplicate": 0,
        "filename_exists": 0,
        "classified_known": 0,
        "classified_keyword": 0,
        "unclassified": 0,
        "written": 0,
    }

    for rec in records:
        if is_excluded(rec["name"]):
            stats["excluded"] += 1
            continue
        if rec["amount_usd"] and rec["amount_usd"] < MIN_AMOUNT_USD:
            stats["too_small"] += 1
            continue

        slug = slugify(rec["name"])
        filename = f"auto_{rec['date']}_{slug}.yaml"
        filepath = os.path.join(out_dir, filename)

        if os.path.exists(filepath):
            stats["filename_exists"] += 1
            continue
        if is_near_duplicate(rec["date"], slug, existing):
            stats["near_duplicate"] += 1
            continue

        data = build_stub(rec)

        if match_known(rec):
            stats["classified_known"] += 1
        elif data["risk_ids"]:
            stats["classified_keyword"] += 1
        else:
            stats["unclassified"] += 1

        if not args.dry_run:
            try:
                write_yaml(filepath, data)
                stats["written"] += 1
                existing.append((rec["date"], slug))
            except OSError as exc:
                print(f"[warn] Could not write {filepath}: {exc}", file=sys.stderr)

    print("\nSummary")
    print("-------")
    for key, val in stats.items():
        print(f"  {key:18s}: {val}")


if __name__ == "__main__":
    main()
