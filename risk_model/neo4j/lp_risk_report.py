#!/usr/bin/env python3
"""Print all risks for an LP depositing a given asset into a given protocol on a given chain.

Pulls risks from the Neo4j risk-model graph across five layers:
  1) Protocol-level active risks        (Protocol -HAS_ACTIVE_RISK-> Risk)
  2) Deployment-specific active risks   (Deployment[chain] -HAS_ACTIVE_RISK-> Risk)
  3) Protocol-type base risks           (ProtocolType -HAS_BASE_RISK-> Risk)
  4) Chain base risks                   (Chain -HAS_BASE_RISK-> Risk)
  5) Asset-level risks                  (Asset -HAS_ASSET_RISK-> Risk; via AssetTaxonomy)
Plus:
  - Upstream dependencies (Protocol/Chain/External) and their base risks
  - Relevant historical incidents (by protocol and by asset)

Usage:
  python lp_risk_report.py
  python lp_risk_report.py --protocol aave_v3 --asset USDC --chain ethereum
  python lp_risk_report.py --protocol compound_v3 --asset USDT --chain arbitrum
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict

try:
    from neo4j import GraphDatabase
except ModuleNotFoundError:
    sys.exit("pip install neo4j  # missing driver")


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


def run(session, cypher, **params):
    return [dict(r) for r in session.run(cypher, **params)]


def section(title: str) -> None:
    print(f"\n{'─' * 78}")
    print(f"  {title}")
    print("─" * 78)


def fmt_risk(row: dict) -> str:
    rid = row.get("risk_id") or row.get("r_risk_id") or "?"
    name = row.get("name") or ""
    src = row.get("source") or ""
    note = row.get("note") or ""
    out = f"  • {rid:<40}"
    if name:
        out += f"  {name}"
    if src:
        out += f"  [{src}]"
    if note:
        out += f"\n      note: {note}"
    return out


def fmt_dollar(n) -> str:
    if not n or n == 0:
        return "near-miss / n/a"
    n = int(n)
    if n >= 1_000_000_000:
        return f"${n/1e9:.1f}B"
    if n >= 1_000_000:
        return f"${n/1e6:.1f}M"
    return f"${n:,}"


def report(session, protocol: str, asset: str, chain: str) -> None:
    protocol_uid = f"protocol:{protocol}"
    deployment_uid = f"deployment:{protocol}.{chain}"
    chain_uid = f"chain:{chain}"
    asset_uid = f"asset:{asset.upper()}"

    # Header: verify targets exist
    hdr = run(
        session,
        """
        OPTIONAL MATCH (p:Protocol {uid:$p})
        OPTIONAL MATCH (d:Deployment {uid:$d})
        OPTIONAL MATCH (c:Chain {uid:$c})
        OPTIONAL MATCH (a:Asset {uid:$a})
        OPTIONAL MATCH (p)-[:HAS_TYPE]->(t:ProtocolType)
        RETURN p.uid AS p, d.uid AS d, c.uid AS c, a.uid AS a, t.uid AS t, t.type_id AS type_id
        """,
        p=protocol_uid, d=deployment_uid, c=chain_uid, a=asset_uid,
    )[0]

    print("=" * 78)
    print(f"  LP Risk Report — supply {asset} into {protocol} on {chain}")
    print("=" * 78)
    missing = [k for k, v in hdr.items() if k in ("p", "d", "c", "a") and not v]
    if missing:
        print(f"  [warn] missing nodes: {missing}")
    print(f"  Protocol:     {hdr.get('p') or '(not in graph)'}")
    print(f"  Deployment:   {hdr.get('d') or '(not in graph)'}")
    print(f"  Chain:        {hdr.get('c') or '(not in graph)'}")
    print(f"  Asset:        {hdr.get('a') or '(not in graph)'}")
    print(f"  Type:         {hdr.get('t') or '(none)'}")

    type_uid = hdr.get("t")

    # 1) Protocol-level active risks
    section("1) Protocol-level active risks  (declared by the protocol file)")
    rows = run(
        session,
        """
        MATCH (p:Protocol {uid:$p})-[rel:HAS_ACTIVE_RISK]->(r:Risk)
        RETURN r.risk_id AS risk_id, r.name AS name, rel.note AS note
        ORDER BY risk_id
        """,
        p=protocol_uid,
    )
    if not rows:
        print("  (none)")
    for r in rows:
        print(fmt_risk({**r, "source": "protocol"}))

    # 2) Deployment-specific active risks
    section(f"2) Deployment-specific active risks  (on {chain})")
    rows = run(
        session,
        """
        MATCH (d:Deployment {uid:$d})-[rel:HAS_ACTIVE_RISK]->(r:Risk)
        RETURN r.risk_id AS risk_id, r.name AS name, rel.note AS note
        ORDER BY risk_id
        """,
        d=deployment_uid,
    )
    if not rows:
        print("  (none)")
    for r in rows:
        print(fmt_risk({**r, "source": "deployment"}))

    # 3) ProtocolType base risks
    section(f"3) Protocol-type base risks  (inherent to {hdr.get('type_id') or '?'})")
    if type_uid:
        rows = run(
            session,
            """
            MATCH (t:ProtocolType {uid:$t})-[rel:HAS_BASE_RISK]->(r:Risk)
            RETURN r.risk_id AS risk_id, r.name AS name, rel.note AS note
            ORDER BY risk_id
            """,
            t=type_uid,
        )
        if not rows:
            print("  (none)")
        for r in rows:
            print(fmt_risk({**r, "source": "type"}))
    else:
        print("  (no protocol type)")

    # 4) Chain base risks
    section(f"4) Chain base risks  ({chain})")
    rows = run(
        session,
        """
        MATCH (c:Chain {uid:$c})-[rel:HAS_BASE_RISK]->(r:Risk)
        RETURN r.risk_id AS risk_id, r.name AS name, rel.note AS note
        ORDER BY risk_id
        """,
        c=chain_uid,
    )
    if not rows:
        print("  (none)")
    for r in rows:
        print(fmt_risk({**r, "source": "chain"}))

    # 5) Asset risks (token-level) — derived from incidents that touched this asset
    section(f"5) Asset-level risks  ({asset}) — evidenced by historical incidents")
    rows = run(
        session,
        """
        MATCH (:Asset {uid:$a})<-[:INVOLVES_ASSET]-(i:Incident)-[:EVIDENCES_RISK]->(r:Risk)
        RETURN DISTINCT r.risk_id AS risk_id, r.name AS name, r.category_id AS category
        ORDER BY category, risk_id
        """,
        a=asset_uid,
    )
    if not rows:
        print("  (no incidents link this asset to taxonomy risks yet)")
    for r in rows:
        cat = f"[{r.get('category') or '?'}] "
        print(f"  • {cat}{r['risk_id']:<40}  {r.get('name') or ''}")

    # 5b) Token-scope taxonomy — baseline risks that apply to tokens in general
    section(f"5b) Token taxonomy baseline  (applicable to any {asset}-like token)")
    rows = run(
        session,
        """
        MATCH (r:Risk {taxonomy_scope:'token'})
        RETURN r.category_id AS category, r.risk_id AS risk_id, r.name AS name
        ORDER BY category, risk_id
        """,
    )
    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r.get("category") or "?"].append(r)
    for cat in sorted(by_cat):
        print(f"\n  [{cat}]")
        for r in by_cat[cat]:
            print(f"    • {r['risk_id']:<40}  {r.get('name') or ''}")

    # 6) Upstream dependencies — what this protocol/deployment relies on
    section("6) Upstream dependencies (risk of any is YOUR risk)")
    deps = run(
        session,
        """
        MATCH (x)-[rel:DEPENDS_ON]->(dep)
        WHERE x.uid IN [$p, $d]
        RETURN DISTINCT labels(dep) AS all_labels, dep.uid AS dep_uid,
               coalesce(dep.name, dep.chain_id, dep.uid) AS label,
               rel.scope AS scope, rel.note AS note
        ORDER BY dep_uid
        """,
        p=protocol_uid, d=deployment_uid,
    )
    if not deps:
        print("  (none)")
    for d in deps:
        kind = [l for l in (d.get("all_labels") or []) if l != "RiskModelNode"]
        kind_str = kind[0] if kind else "Node"
        scope = f"  scope={d['scope']}" if d.get("scope") else ""
        note = f"\n      {d['note']}" if d.get("note") else ""
        print(f"  • [{kind_str}] {d['dep_uid']}{scope}{note}")

    # 6b) Risks that any dependency brings in (transitive)
    section("6b) Transitive risks from dependencies")
    tr = run(
        session,
        """
        MATCH (x)-[:DEPENDS_ON]->(dep)-[:HAS_ACTIVE_RISK|HAS_BASE_RISK]->(r:Risk)
        WHERE x.uid IN [$p, $d]
        RETURN DISTINCT dep.uid AS dep_uid, r.risk_id AS risk_id, r.name AS name
        ORDER BY dep_uid, risk_id
        """,
        p=protocol_uid, d=deployment_uid,
    )
    if not tr:
        print("  (none)")
    for r in tr:
        print(f"  • {r['risk_id']:<40}  via {r['dep_uid']}   {r.get('name') or ''}")

    # 7) Historical incidents touching this protocol or this asset
    section("7) Historical incidents touching protocol or asset")
    inc = run(
        session,
        """
        MATCH (i:Incident)
        WHERE (i)-[:INVOLVES_PROTOCOL]->(:Protocol {uid:$p})
           OR (i)-[:INVOLVES_ASSET]->(:Asset {uid:$a})
        OPTIONAL MATCH (i)-[:EVIDENCES_RISK]->(r:Risk)
        RETURN i.uid AS uid, i.title AS title, i.date AS date,
               i.amount_lost_usd AS amt, i.event_type AS evt,
               collect(DISTINCT r.risk_id) AS evidenced
        ORDER BY date DESC
        """,
        p=protocol_uid, a=asset_uid,
    )
    if not inc:
        print("  (none)")
    for r in inc:
        print(f"  • {r['date']}  {r['title']}  ({fmt_dollar(r['amt'])})")
        if r.get("evidenced"):
            print(f"      evidences: {', '.join(r['evidenced'])}")

    # 8) Union / deduped list of all risk_ids touching the LP position
    section("8) Consolidated risk set (deduplicated)")
    union = run(
        session,
        """
        MATCH (r:Risk)
        WHERE EXISTS {
            MATCH (:Protocol {uid:$p})-[:HAS_ACTIVE_RISK]->(r)
        } OR EXISTS {
            MATCH (:Deployment {uid:$d})-[:HAS_ACTIVE_RISK]->(r)
        } OR EXISTS {
            MATCH (:ProtocolType {uid:$t})-[:HAS_BASE_RISK]->(r)
        } OR EXISTS {
            MATCH (:Chain {uid:$c})-[:HAS_BASE_RISK]->(r)
        } OR EXISTS {
            MATCH (:Asset {uid:$a})<-[:INVOLVES_ASSET]-(:Incident)-[:EVIDENCES_RISK]->(r)
        } OR EXISTS {
            MATCH (x)-[:DEPENDS_ON]->()-[:HAS_ACTIVE_RISK|HAS_BASE_RISK]->(r)
            WHERE x.uid IN [$p, $d]
        }
        RETURN DISTINCT r.risk_id AS risk_id, r.name AS name, r.category_id AS category
        ORDER BY category, risk_id
        """,
        p=protocol_uid, d=deployment_uid, t=type_uid or "", c=chain_uid, a=asset_uid,
    )
    by_cat = defaultdict(list)
    for r in union:
        by_cat[r.get("category") or "uncategorized"].append(r)
    for cat in sorted(by_cat):
        print(f"\n  [{cat}]")
        for r in by_cat[cat]:
            print(f"    • {r['risk_id']:<40}  {r.get('name') or ''}")
    print(f"\n  Total distinct risks: {len(union)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--protocol", default="aave_v3", help="protocol slug (default: aave_v3)")
    ap.add_argument("--asset",    default="USDC",    help="asset symbol  (default: USDC)")
    ap.add_argument("--chain",    default="ethereum",help="chain slug    (default: ethereum)")
    args = ap.parse_args()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        report(session, args.protocol, args.asset, args.chain)
    driver.close()


if __name__ == "__main__":
    main()
