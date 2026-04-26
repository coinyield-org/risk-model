"""
bootstrap_defillama.py

Parses the SunWeb3Sec/DeFiHackLabs GitHub README files and generates auto_*.yaml
incident stubs for events that map to known risk taxonomy IDs.

Note: The DefiLlama hacks API (https://api.llama.fi/hacks) moved to a paid tier
in 2025. This script uses the SunWeb3Sec/DeFiHackLabs repository as a free
alternative (689+ incidents, regularly updated).

Usage (from repo root):
    python risk_model/incidents/bootstrap_defillama.py
    python risk_model/incidents/bootstrap_defillama.py --out-dir /path/to/incidents
"""

import argparse
import os
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUEST_TIMEOUT = 30
DEFIHACKLABS_BASE = "https://raw.githubusercontent.com/SunWeb3Sec/DeFiHackLabs/main"

# Year-specific README files (2020-2025) + main README (2026+)
README_URLS = [
    f"{DEFIHACKLABS_BASE}/past/{year}/README.md"
    for year in range(2020, 2026)
] + [f"{DEFIHACKLABS_BASE}/README.md"]

KNOWN_PROTOCOL_SLUGS = [
    "aave_v3", "arbitrum_bridge", "aster_bridge", "babylon", "base_bridge",
    "bedrock", "binance_btc", "bouncebit", "buzz_farming", "cap",
    "coinbase_bridge", "coinbase_cbeth", "compound_v3", "convex", "curve",
    "eigenlayer", "ethena", "etherfi", "etherfi_liquid", "frax",
    "free_protocol", "grove_finance", "hyperlend", "hyperliquid",
    "hyperliquid_hlp", "jupiter_lend", "jupiter_perps", "jupiter_staked_sol",
    "justlend", "kamino", "kelp", "kraken_bitcoin", "lido", "lombard_lbtc",
    "m0", "maple", "mellow", "meth_protocol", "morpho", "ondo",
    "optimism_bridge", "pancakeswap", "pendle", "polygon_bridge",
    "portal_wormhole", "renzo", "rocket_pool", "sky_lending", "solv_btc",
    "spark_liquidity", "sparklend", "ssv_network", "stacks_sbtc", "stader",
    "steakhouse", "symbiotic", "tbtc", "tornado_cash", "unirouter",
    "uniswap_v3", "uniswap_v4", "upshift", "venus", "wbeth", "wbtc", "yearn",
]


# Generic tokens that must never map to a protocol slug by themselves.
# Without this filter the substring match promotes "bridge" → "arbitrum_bridge"
# for any incident whose name contains "bridge" (Kinto Bridge, Heco Bridge, ...).
_GENERIC_TOKENS = {
    "bridge", "chain", "network", "finance", "protocol", "dao", "token",
    "swap", "pool", "vault", "lending", "perps", "perp",
}


def _build_slug_index(slugs):
    index = {}
    for slug in slugs:
        parts = slug.split("_")
        key_full = slug.replace("_", "")
        index.setdefault(key_full, slug)
        for part in parts:
            if len(part) >= 4 and part not in _GENERIC_TOKENS:
                index.setdefault(part, slug)
    return index


_SLUG_INDEX = _build_slug_index(KNOWN_PROTOCOL_SLUGS)

# Explorer domain -> chain ID
EXPLORER_CHAIN_MAP = {
    "etherscan.io": "ethereum",
    "bscscan.com": "bnb",
    "arbiscan.io": "arbitrum",
    "polygonscan.com": "polygon",
    "optimistic.etherscan.io": "optimism",
    "basescan.org": "base",
    "snowtrace.io": "avalanche",
    "avascan.io": "avalanche",
    "ftmscan.com": "fantom",
    "solscan.io": "solana",
    "explorer.solana.com": "solana",
    "tronscan.org": "tron",
    "gnosisscan.io": "gnosis",
    "lineascan.build": "linea",
    "mantlescan.xyz": "mantle",
}

# ---------------------------------------------------------------------------
# Attack type classification -> risk_ids
# ---------------------------------------------------------------------------

# Patterns that make an entry OUT OF SCOPE (pure code / smart-contract bugs).
# Checked before in-scope patterns. Uses lowercase substring matching.
_OUT_OF_SCOPE_PATTERNS = [
    "reentrancy", "re-entrancy",
    "flash loan", "flashloan", "flash mint", "flashmint",
    "logic flaw", "business logic", "logic error",
    "integer overflow", "integer underflow", "integer truncation",
    "improper input", "incorrect input", "incorrect output",
    "arbitrary external call",
    "donation attack",
    "precision loss", "unit mismatch",
    "incorrect fee", "incorrect token", "incorrect burn", "incorrect reward",
    "incorrect dividend", "incorrect calculation",
    "burn mechanism", "burn logic",
    "access control",   # DeFiHackLabs uses this for contract-level ACL bugs
    "lack of access",
    "share price manipulation",  # typically precision/rounding bugs
]

# Ordered: first matching rule wins; returns (risk_ids, event_type)
_IN_SCOPE_RULES = [
    # Oracle / price manipulation
    (["oracle", "price oracle", "twap oracle", "overpriced asset", "price dependency",
      "vulnerable price", "oracle price"],
     ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
     "oracle_failure"),
    # Price manipulation without "oracle" keyword — still oracle-class risk
    (["price manipulation"],
     ["thin_liquidity_source_manipulation", "quoted_vs_underlying_depeg"],
     "oracle_failure"),
    # Bridge hacks
    (["bridge"],
     ["bridge_dep", "bridge_signing_committee"],
     "bridge"),
    # Governance attacks
    (["governance"],
     ["flash_governance", "hostile_proposal_via_delegation"],
     "governance"),
    # Rug pulls / exit scams
    (["rug pull", "rug", "exit scam"],
     ["governance_hostile_decision", "deployer_key_leak"],
     "governance"),
    # Private key / signer compromise
    (["private key", "key compromise", "key leak"],
     ["governance_signer_key_leak", "deployer_key_leak"],
     "exploit"),
    # Algorithmic stablecoin / depeg
    (["depeg", "algo stablecoin", "algorithmic stablecoin", "death spiral"],
     ["stablecoin_depeg", "soft_peg_algo_failure"],
     "depeg"),
]


def classify_attack_type(attack_type: str):
    """
    Return (risk_ids, event_type) for a DeFiHackLabs attack type string,
    or ([], None) when the event is out of scope.
    """
    low = attack_type.lower()

    for pattern in _OUT_OF_SCOPE_PATTERNS:
        if pattern in low:
            return [], None

    for keywords, risk_ids, event_type in _IN_SCOPE_RULES:
        if any(kw in low for kw in keywords):
            return risk_ids, event_type

    return [], None

# ---------------------------------------------------------------------------
# Amount parsing
# ---------------------------------------------------------------------------

def parse_amount_usd(lost_str: str) -> int:
    """
    Parse a USD amount from DeFiHackLabs "Lost:" strings.
    Examples:
        "15.7k USD"          -> 15700
        "~$7M"               -> 7000000
        "~88M US$"           -> 88000000
        "$230,000"           -> 230000
        "17.4 BNB (~$12k)"   -> 12000   (parenthetical USD wins)
        "~384 BNB"           -> 0       (non-USD, no fallback)
    """
    if not lost_str:
        return 0

    s = lost_str.strip()

    # 1. Prefer USD amount in parentheses: (~$3.8M USD) or (>$3.8M USD)
    paren = re.search(r'\(\s*[~>]?\s*\$?([\d,\.]+)\s*([kKmMbB]?)\s*(?:USD|US\$)?\s*\)', s)
    if paren:
        return _parse_value(paren.group(1), paren.group(2))

    # 2. Explicit USD pattern: $7M, $230,000, 15.7k USD, 88M US$
    usd = re.search(
        r'[~>]?\s*\$?([\d,\.]+)\s*([kKmMbB]?)\s*(?:USD|US\$|USDT|USDC|k USD|M USD)',
        s, re.IGNORECASE
    )
    if usd:
        return _parse_value(usd.group(1), usd.group(2))

    # 3. Bare number with k/M/B suffix (no explicit currency — assume USD if no token name)
    bare = re.search(r'^\s*[~>]?\s*\$?([\d,\.]+)\s*([kKmMbB]?)\s*$', s)
    if bare:
        return _parse_value(bare.group(1), bare.group(2))

    return 0


def _parse_value(digits: str, suffix: str) -> int:
    try:
        value = float(digits.replace(",", ""))
    except ValueError:
        return 0
    mult = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(suffix.lower(), 1)
    return int(value * mult)

# ---------------------------------------------------------------------------
# Chain inference from link reference URLs
# ---------------------------------------------------------------------------

def infer_chain_from_url(url: str) -> str | None:
    if not url:
        return None
    url_low = url.lower()
    for domain, chain_id in EXPLORER_CHAIN_MAP.items():
        if domain in url_low:
            return chain_id
    return None

# ---------------------------------------------------------------------------
# Helpers: slugify, protocol matching
# ---------------------------------------------------------------------------

def slugify(name: str, max_chars: int = 30) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s[:max_chars].rstrip("_")


def match_protocol_slugs(name: str) -> list[str]:
    if not name:
        return []
    normalised = name.lower()
    for noise in (" finance", " protocol", " exchange", " network", " dao"):
        normalised = normalised.replace(noise, "")
    normalised = normalised.strip()
    matched: set[str] = set()
    slug_candidate = re.sub(r"[^a-z0-9]+", "_", normalised).strip("_")
    if slug_candidate in set(KNOWN_PROTOCOL_SLUGS):
        matched.add(slug_candidate)
    name_clean = re.sub(r"[^a-z0-9]", "", normalised)
    # Require slug_clean to be at least 5 chars for substring matching.
    # Without this, short slugs like "cap" match "Rari Capital" via the "cap"
    # prefix inside "capital", and short names like "un" match every slug
    # containing the letters "un" (unirouter, uniswap_v3, bouncebit, ...).
    for slug in KNOWN_PROTOCOL_SLUGS:
        slug_clean = slug.replace("_", "")
        if len(slug_clean) < 5 or len(name_clean) < 5:
            continue
        if name_clean in slug_clean or slug_clean in name_clean:
            matched.add(slug)
    tokens = re.split(r"[^a-z0-9]+", normalised)
    for token in tokens:
        if len(token) >= 4 and token in _SLUG_INDEX:
            matched.add(_SLUG_INDEX[token])
    return sorted(matched)

# ---------------------------------------------------------------------------
# YAML serialisation (stdlib-only, same as original)
# ---------------------------------------------------------------------------

def _yaml_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return '""'
    s = str(value)
    if not s or any(c in s for c in ':#{}&*!,[]|>\'"\\%@`\n\r\t'):
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    if s.lower() in ("true", "false", "null", "yes", "no", "on", "off"):
        return f'"{s}"'
    return s


def _render_yaml(data: dict) -> str:
    lines = []

    def str_list(lst, indent=2):
        if not lst:
            return "[]"
        pad = " " * indent
        items = "\n".join(f"{pad}- {_yaml_scalar(item)}" for item in lst)
        return f"\n{items}"

    field_order = [
        "id", "title", "date", "event_type", "amount_lost_usd", "near_miss",
        "affected_protocols", "affected_assets", "chains", "root_cause_entity",
        "cascade_targets", "risk_ids", "source_urls", "confidence", "notes",
    ]
    list_fields = {
        "affected_protocols", "affected_assets", "chains",
        "cascade_targets", "risk_ids", "source_urls",
    }
    for key in field_order:
        if key not in data:
            continue
        value = data[key]
        if key in list_fields:
            lines.append(f"{key}:{str_list(value)}")
        else:
            lines.append(f"{key}: {_yaml_scalar(value)}")
    return "\n".join(lines) + "\n"


def write_yaml(path: str, data: dict) -> None:
    header = "# Auto-generated by bootstrap_defillama.py — review and update confidence before use\n"
    try:
        import yaml  # type: ignore

        def str_representer(dumper, data):
            if "\n" in data:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)

        class NiceDumper(yaml.Dumper):
            pass

        NiceDumper.add_representer(str, str_representer)
        body = yaml.dump(data, Dumper=NiceDumper, default_flow_style=False,
                         allow_unicode=True, sort_keys=False)
        content = header + body
    except ImportError:
        content = header + _render_yaml(data)

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

# ---------------------------------------------------------------------------
# DeFiHackLabs README parsing
# ---------------------------------------------------------------------------

# Header: "### YYYYMMDD ProtocolName - AttackType"
# Variant: "### YYYYMMDD - ProtocolName - AttackType" (extra dash)
_HEADER_RE = re.compile(
    r'^#{1,4}\s+(\d{8})\s+(?:-\s+)?(.+?)\s+-\s+(.+)',
    re.MULTILINE,
)
_LOST_RE = re.compile(r'^#{1,4}\s+Lost[:\s]+(.+)', re.MULTILINE | re.IGNORECASE)
_URL_RE = re.compile(r'https?://\S+')


def fetch_readme(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "coinyield-bootstrap/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_readme(content: str) -> list[dict]:
    """
    Parse a DeFiHackLabs README and return a list of raw incident dicts with keys:
        date_raw, name, attack_type, lost_str, source_url
    """
    records = []

    # Split on horizontal rules (---) that separate incidents
    blocks = re.split(r'\n---+\n', content)

    for block in blocks:
        m = _HEADER_RE.search(block)
        if not m:
            continue

        date_raw = m.group(1)   # YYYYMMDD
        name = m.group(2).strip()
        attack_type = m.group(3).strip()

        # Skip table-of-contents anchor references embedded in main README TOC
        if name.startswith("[") or attack_type.startswith("["):
            continue

        lost_m = _LOST_RE.search(block)
        lost_str = lost_m.group(1).strip() if lost_m else ""

        urls = _URL_RE.findall(block)
        # Prefer block-explorer URLs for chain detection; keep first URL as source
        source_url = urls[0] if urls else ""

        records.append({
            "date_raw": date_raw,
            "name": name,
            "attack_type": attack_type,
            "lost_str": lost_str,
            "source_url": source_url,
            "all_urls": urls,
        })

    return records


def date_raw_to_str(date_raw: str) -> str:
    """Convert YYYYMMDD to YYYY-MM-DD."""
    if len(date_raw) == 8 and date_raw.isdigit():
        return f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:8]}"
    return "1970-01-01"

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Bootstrap incident YAML stubs from DeFiHackLabs GitHub READMEs."
    )
    default_out = os.path.dirname(os.path.abspath(__file__))
    parser.add_argument(
        "--out-dir", default=default_out,
        help=f"Directory to write YAML files into (default: {default_out}).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_dir = os.path.abspath(args.out_dir)

    if not os.path.isdir(out_dir):
        print(f"[error] Output directory does not exist: {out_dir}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url in README_URLS:
        print(f"Fetching {url} ...")
        try:
            content = fetch_readme(url)
            records = parse_readme(content)
            print(f"  Parsed {len(records)} entries.")
            all_records.extend(records)
        except Exception as exc:
            print(f"  [warn] Could not fetch/parse {url}: {exc}", file=sys.stderr)

    total_fetched = len(all_records)
    print(f"\nTotal parsed: {total_fetched} entries across all READMEs.")

    # De-duplicate by (date_raw, name) — same incident may appear in multiple READMEs
    seen_keys: set[tuple] = set()
    deduped: list[dict] = []
    for rec in all_records:
        key = (rec["date_raw"], rec["name"].lower())
        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(rec)
    print(f"After deduplication: {len(deduped)} unique entries.")

    kept = []
    skipped_scope = 0
    skipped_amount = 0

    MIN_AMOUNT_USD = 10_000  # skip tiny incidents

    for rec in deduped:
        risk_ids, event_type = classify_attack_type(rec["attack_type"])
        if not risk_ids:
            skipped_scope += 1
            continue

        amount = parse_amount_usd(rec["lost_str"])
        if amount < MIN_AMOUNT_USD:
            skipped_amount += 1
            continue

        kept.append((rec, risk_ids, event_type, amount))

    print(f"Filtered out: {skipped_scope} out-of-scope, {skipped_amount} below ${MIN_AMOUNT_USD:,}.")
    print(f"Keeping {len(kept)} records.\n")

    written = 0
    skipped_existing = 0

    for rec, risk_ids, event_type, amount in kept:
        date_str = date_raw_to_str(rec["date_raw"])
        name = rec["name"]
        slug = slugify(name)
        filename = f"auto_{date_str}_{slug}.yaml"
        filepath = os.path.join(out_dir, filename)

        if os.path.exists(filepath):
            skipped_existing += 1
            continue

        # Chain: try to infer from any URL in the block
        chain_id = None
        for url in rec.get("all_urls", []):
            chain_id = infer_chain_from_url(url)
            if chain_id:
                break
        chains = [chain_id] if chain_id else []

        affected_protocols = match_protocol_slugs(name)
        source_urls = [rec["source_url"]] if rec["source_url"] else []

        incident_id = f"incident:{date_str}_{slug}"
        data = {
            "id": incident_id,
            "title": name,
            "date": date_str,
            "event_type": event_type,
            "amount_lost_usd": amount,
            "near_miss": False,
            "affected_protocols": affected_protocols,
            "affected_assets": [],
            "chains": chains,
            "root_cause_entity": "",
            "cascade_targets": [],
            "risk_ids": risk_ids,
            "source_urls": source_urls,
            "confidence": "low",
            "notes": (
                f"Auto-generated from DeFiHackLabs. "
                f"Attack type: {rec['attack_type']}. "
                f"Review and update confidence before use."
            ),
        }

        try:
            write_yaml(filepath, data)
            written += 1
        except OSError as exc:
            print(f"[warn] Could not write {filepath}: {exc}", file=sys.stderr)

    print("Summary")
    print("-------")
    print(f"  Total fetched   : {total_fetched}")
    print(f"  After dedup     : {len(deduped)}")
    print(f"  After filtering : {len(kept)}")
    print(f"  Written         : {written}")
    if skipped_existing:
        print(f"  Skipped (exist) : {skipped_existing}")
    print(f"  Output dir      : {out_dir}")


if __name__ == "__main__":
    main()
