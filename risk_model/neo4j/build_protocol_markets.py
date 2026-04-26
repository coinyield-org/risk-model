#!/usr/bin/env python3
"""
Build risk_model/neo4j/protocol_markets.json — maps our 97 protocol slugs
to their market/pool records from DeFiLlama yields data.

Output: protocol_markets.json
  {
    "aave_v3": [
      { "pool_id": "uuid", "chain": "ethereum", "symbol": "WETH",
        "tvl_usd": 1.5e9, "apy": 2.5, "apy_base": 2.1, "apy_reward": 0.4,
        "underlying_tokens": [...], "token_symbols": [...], "il_risk": "no",
        "stablecoin": false },
      ...
    ],
    ...
  }
"""

import json
import re
from pathlib import Path

RISK_ROOT = Path(__file__).parent.parent
DEX_POOLS_DIR = RISK_ROOT.parent / "dex_pools"
OUT_PATH = Path(__file__).parent / "protocol_markets.json"

# Explicit overrides where auto-mapping fails
SLUG_OVERRIDES: dict[str, str | list[str]] = {
    "aave_v3":          "aave-v3",
    "compound_v3":      "compound-v3",
    "curve":            "curve-dex",
    "uniswap_v3":       "uniswap-v3",
    "uniswap_v4":       "uniswap-v4",
    "pancakeswap":      ["pancakeswap-amm-v3", "pancakeswap-amm"],
    "morpho":           "morpho-blue",
    "yearn":            "yearn-finance",
    "convex":           "convex-finance",
    "etherfi":          "ether.fi",
    "etherfi_liquid":   "ether.fi-liquid",
    "sky_lending":      ["sky", "sky-lending"],
    "spark_liquidity":  ["spark", "sparklend"],
    "sparklend":        "sparklend",
    "jupiter_lend":     "jupiter-lend",
    "jupiter_perps":    "jupiter-perpetual-exchange",
    "jupiter_staked_sol": "jito-staked-sol",
    "hyperliquid_hlp":  "hyperliquid-hlp",
    "hyperlend":        "hyperlend",
    "rocket_pool":      "rocket-pool",
    "ssv_network":      "ssv-network",
    "meth_protocol":    "mantle-lsd",
    "wbeth":            "binance-staked-eth",
    "grove_finance":    "grove",
    "free_protocol":    "free-protocol",
    "buzz_farming":     "buzz",
    "upshift":          "upshift",
    "steakhouse":       "steakhouse-financial",
    "portal_wormhole":  "wormhole",
    "tornado_cash":     None,   # no pool data
    "m0":               None,
    "stacks_sbtc":      None,
    "merlin_chain":     None,
}


def auto_slug(our_slug: str) -> str:
    """Convert our_slug to DeFiLlama slug: underscores → hyphens."""
    return our_slug.replace("_", "-")


def read_protocol_slugs() -> list[str]:
    slugs = []
    for f in sorted((RISK_ROOT / "protocols").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^slug:\s*(\S+)", text, re.MULTILINE)
        if m:
            slugs.append(m.group(1).strip())
    return slugs


def load_all_pools() -> dict[str, list[dict]]:
    """Load all enriched pool files, keyed by DeFiLlama project slug."""
    by_project: dict[str, list[dict]] = {}
    for jf in DEX_POOLS_DIR.glob("*/top100_by_protocol_enriched.json"):
        data = json.loads(jf.read_text(encoding="utf-8"))
        for proto, pools in data["data"].items():
            by_project.setdefault(proto, []).extend(pools)
    # Also try non-enriched fallback
    for jf in DEX_POOLS_DIR.glob("*/top100_by_protocol.json"):
        data = json.loads(jf.read_text(encoding="utf-8"))
        for proto, pools in data["data"].items():
            if proto not in by_project:
                by_project[proto] = pools
    return by_project


def trim_pool(pool: dict) -> dict:
    """Keep only fields relevant for graph nodes."""
    return {
        "pool_id":          pool.get("pool"),
        "chain":            pool.get("chain"),
        "symbol":           pool.get("symbol"),
        "tvl_usd":          pool.get("tvlUsd"),
        "apy":              pool.get("apy"),
        "apy_base":         pool.get("apyBase"),
        "apy_reward":       pool.get("apyReward"),
        "il_risk":          pool.get("ilRisk"),
        "stablecoin":       pool.get("stablecoin"),
        "underlying_tokens": pool.get("underlyingTokens") or [],
        "token_symbols":    pool.get("token_symbols") or [],
        "token_prices":     pool.get("token_prices") or [],
        "volume_usd_1d":    pool.get("volumeUsd1d"),
        "apy_mean_30d":     pool.get("apyMean30d"),
    }


def main() -> None:
    our_slugs = read_protocol_slugs()
    print(f"Our protocol slugs: {len(our_slugs)}")

    all_pools = load_all_pools()
    available = set(all_pools.keys())
    print(f"DeFiLlama projects with pool data: {len(available)}")

    result: dict[str, list[dict]] = {}
    matched = []
    unmatched = []

    for slug in our_slugs:
        # Determine candidate DL slugs
        if slug in SLUG_OVERRIDES:
            override = SLUG_OVERRIDES[slug]
            if override is None:
                candidates = []
            elif isinstance(override, list):
                candidates = override
            else:
                candidates = [override]
        else:
            candidates = [auto_slug(slug), slug]

        pools = []
        matched_as = None
        for cand in candidates:
            if cand in available:
                pools = all_pools[cand]
                matched_as = cand
                break

        if pools:
            result[slug] = [trim_pool(p) for p in pools]
            matched.append((slug, matched_as, len(pools)))
        else:
            unmatched.append(slug)

    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nMatched: {len(matched)}")
    for slug, dl_slug, n in matched:
        print(f"  {slug:<30} → {dl_slug:<35} ({n} pools)")

    print(f"\nUnmatched ({len(unmatched)}):")
    for slug in unmatched:
        print(f"  {slug}")

    print(f"\nWrote {OUT_PATH}")
    print(f"Total market records: {sum(len(v) for v in result.values())}")


if __name__ == "__main__":
    main()
