#!/usr/bin/env python3
"""Generate Neo4j Cypher import for coinyield risk_model.

The importer intentionally does not connect to Neo4j. It produces a deterministic
Cypher file that can be reviewed, committed, and loaded with cypher-shell.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyYAML is required. Run with the conda Python that has PyYAML installed, "
        "or install pyyaml in your active environment."
    ) from exc


RISK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = Path(__file__).resolve().parent / "generated" / "risk_model.cypher"


@dataclass
class Node:
    uid: str
    labels: set[str] = field(default_factory=set)
    props: dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    source_uid: str
    rel_type: str
    target_uid: str
    uid: str
    props: dict[str, Any] = field(default_factory=dict)


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.relationships: dict[tuple[str, str, str, str], Relationship] = {}
        self.warnings: list[str] = []

    def add_node(self, uid: str, labels: list[str], props: dict[str, Any] | None = None) -> None:
        node = self.nodes.setdefault(uid, Node(uid=uid))
        node.labels.update(labels)
        node.labels.add("RiskModelNode")
        node.props["uid"] = uid
        if props:
            for key, value in props.items():
                if value is not None:
                    node.props[key] = normalize_value(value)

    def add_rel(
        self,
        source_uid: str,
        rel_type: str,
        target_uid: str,
        uid: str,
        props: dict[str, Any] | None = None,
    ) -> None:
        key = (source_uid, rel_type, target_uid, uid)
        rel = self.relationships.setdefault(
            key, Relationship(source_uid=source_uid, rel_type=rel_type, target_uid=target_uid, uid=uid)
        )
        rel.props["uid"] = uid
        if props:
            for prop_key, value in props.items():
                if value is not None:
                    rel.props[prop_key] = normalize_value(value)


def normalize_slug(value: str) -> str:
    value = value.strip()
    value = value.replace("&", " and ")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_").lower()


def normalize_value(value: Any) -> Any:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, tuple):
        return [normalize_value(item) for item in value]
    if isinstance(value, list):
        return [normalize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(k): normalize_value(v) for k, v in value.items()}
    return value


def cypher_literal(value: Any) -> str:
    value = normalize_value(value)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(cypher_literal(v) for v in value) + "]"
    if isinstance(value, dict):
        items = []
        for key in sorted(value):
            items.append(f"{safe_prop_key(key)}: {cypher_literal(value[key])}")
        return "{" + ", ".join(items) + "}"
    text = str(value)
    text = text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
    return f"'{text}'"


def safe_prop_key(key: str) -> str:
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
        return key
    return f"`{key.replace('`', '``')}`"


def props_literal(props: dict[str, Any]) -> str:
    clean = {key: value for key, value in props.items() if value is not None}
    return cypher_literal(clean)


def labels_literal(labels: set[str]) -> str:
    return "".join(f":{label}" for label in sorted(labels))


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    data = load_yaml_tolerant(parts[1], path) or {}
    return data, parts[2]


def read_yaml(path: Path) -> dict[str, Any]:
    return load_yaml_tolerant(path.read_text(encoding="utf-8"), path) or {}


def load_yaml_tolerant(text: str, path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return yaml.safe_load(quote_text_scalars(text)) or {}


def quote_text_scalars(text: str) -> str:
    """Quote common human-text scalar fields that contain YAML-hostile chars.

    Several existing taxonomy files are written as YAML-like authoring files and
    contain plain scalar descriptions with ": ". PyYAML correctly rejects those,
    but preserving the source format is more useful than mass-editing taxonomy
    prose only for importer compatibility.
    """

    text_keys = {
        "name",
        "description",
        "note",
        "theoretical_basis",
    }
    quoted_lines: list[str] = []
    pattern = re.compile(r"^(\s*)([A-Za-z_][A-Za-z0-9_]*):\s+(.+?)\s*$")
    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            quoted_lines.append(line)
            continue
        indent, key, value = match.groups()
        stripped = value.strip()
        if key not in text_keys or stripped.startswith(("[", "{", "|", ">")):
            quoted_lines.append(line)
            continue
        if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
            stripped = stripped[1:-1]
        quoted_lines.append(f"{indent}{key}: {json.dumps(stripped, ensure_ascii=False)}")
    return "\n".join(quoted_lines) + "\n"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def rel_scope_targets(protocol_slug: str, deployments: list[dict[str, Any]], scope: Any) -> list[str]:
    protocol_uid = f"protocol:{protocol_slug}"
    if not deployments:
        return [protocol_uid]

    if scope in (None, "protocol"):
        return [protocol_uid]

    if scope == "all_deployments":
        return [f"deployment:{protocol_slug}.{deployment.get('chain')}" for deployment in deployments if deployment.get("chain")]

    scopes = as_list(scope)
    targets = []
    deployment_chains = {deployment.get("chain") for deployment in deployments}
    for item in scopes:
        if item == "all_deployments":
            targets.extend(
                f"deployment:{protocol_slug}.{deployment.get('chain')}"
                for deployment in deployments
                if deployment.get("chain")
            )
        elif item in deployment_chains:
            targets.append(f"deployment:{protocol_slug}.{item}")
        else:
            targets.append(protocol_uid)
    return sorted(set(targets))


def risk_targets(protocol_slug: str, deployments: list[dict[str, Any]], deployment_value: Any) -> list[str]:
    return rel_scope_targets(protocol_slug, deployments, deployment_value)


def dependency_target_uid(dep_id: str, protocol_slugs: set[str], chain_ids: set[str]) -> tuple[str, list[str]]:
    if dep_id in protocol_slugs:
        return f"protocol:{dep_id}", ["Protocol"]
    if dep_id in chain_ids:
        return f"chain:{dep_id}", ["Chain"]
    return f"dependency:{dep_id}", ["ExternalDependency"]


def asset_uid(raw: str) -> tuple[str, list[str], dict[str, Any]]:
    symbol = str(raw).strip()
    if "/" in symbol:
        slug = normalize_slug(symbol)
        return f"price_pair:{slug}", ["PricePair"], {"pair": symbol, "pair_id": slug}
    symbol_upper = symbol.upper()
    return f"asset:{symbol_upper}", ["Asset"], {"symbol": symbol_upper, "asset_id": symbol_upper}


def flatten_severity(prefix: str, severity: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(severity, dict):
        return {}
    return {f"{prefix}_{key}": value for key, value in severity.items() if not isinstance(value, (dict, list))}


def add_taxonomy(graph: Graph, risk_root: Path) -> set[str]:
    known_risks: set[str] = set()
    for taxonomy_path in sorted((risk_root / "taxonomy").glob("*_risks.yaml")):
        data = read_yaml(taxonomy_path)
        scope = data.get("scope")
        for category in data.get("categories", []):
            category_id = category.get("id")
            if not category_id:
                continue
            category_uid = f"risk_category:{category_id}"
            graph.add_node(
                category_uid,
                ["RiskCategory"],
                {
                    "category_id": category_id,
                    "name": category.get("name"),
                    "description": category.get("description"),
                    "taxonomy_scope": scope,
                    "source_path": str(taxonomy_path.relative_to(risk_root)),
                },
            )
            for risk in category.get("risks", []):
                risk_id = risk.get("id")
                if not risk_id:
                    continue
                known_risks.add(risk_id)
                risk_uid = f"risk:{risk_id}"
                graph.add_node(
                    risk_uid,
                    ["Risk"],
                    {
                        "risk_id": risk_id,
                        "name": risk.get("name"),
                        "description": risk.get("description"),
                        "category_id": category_id,
                        "taxonomy_scope": scope,
                        "taxonomy_defined": True,
                        "source_path": str(taxonomy_path.relative_to(risk_root)),
                    },
                )
                graph.add_rel(
                    risk_uid,
                    "IN_CATEGORY",
                    category_uid,
                    f"{risk_uid}:in_category:{category_id}",
                    {"source_path": str(taxonomy_path.relative_to(risk_root))},
                )
    return known_risks


def ensure_risk(graph: Graph, risk_id: str, known_risks: set[str], source_path: str) -> None:
    risk_uid = f"risk:{risk_id}"
    if risk_id not in known_risks:
        graph.warnings.append(f"unknown risk_id {risk_id} referenced by {source_path}")
        graph.add_node(
            risk_uid,
            ["Risk"],
            {
                "risk_id": risk_id,
                "taxonomy_defined": False,
                "source_path": source_path,
            },
        )


def add_detailed_risks(graph: Graph, risk_root: Path) -> None:
    for path in sorted((risk_root / "risks").glob("*.md")):
        fm, _body = read_frontmatter(path)
        risk_id = fm.get("id") or path.stem
        props = {
            "risk_id": risk_id,
            "name": fm.get("name"),
            "category_id": fm.get("category"),
            "applies_to": fm.get("applies_to"),
            "related_risks": fm.get("related_risks"),
            "incidents": json.dumps(normalize_value(fm.get("incidents", [])), ensure_ascii=False),
            "source_path": str(path.relative_to(risk_root)),
        }
        props.update(flatten_severity("base", fm.get("severity")))
        graph.add_node(f"risk:{risk_id}", ["Risk"], props)


def add_types(graph: Graph, risk_root: Path, known_risks: set[str]) -> set[str]:
    type_ids: set[str] = set()
    for path in sorted((risk_root / "types").glob("*.md")):
        fm, _body = read_frontmatter(path)
        type_id = fm.get("id") or path.stem
        type_ids.add(type_id)
        type_uid = f"type:{type_id}"
        graph.add_node(
            type_uid,
            ["ProtocolType"],
            {
                "type_id": type_id,
                "name": fm.get("name"),
                "description": fm.get("description"),
                "examples": fm.get("examples"),
                "key_parameters": fm.get("key_parameters"),
                "key_invariants": fm.get("key_invariants"),
                "attack_patterns": fm.get("attack_patterns"),
                "source_path": str(path.relative_to(risk_root)),
            },
        )
        for risk_id in fm.get("key_risks", []) or []:
            ensure_risk(graph, risk_id, known_risks, str(path.relative_to(risk_root)))
            graph.add_rel(
                type_uid,
                "HAS_BASE_RISK",
                f"risk:{risk_id}",
                f"{type_uid}:base_risk:{risk_id}",
                {"source_path": str(path.relative_to(risk_root))},
            )
    return type_ids


def add_chains(graph: Graph, risk_root: Path, known_risks: set[str]) -> set[str]:
    chain_ids: set[str] = set()
    for path in sorted((risk_root / "chains").glob("*.md")):
        fm, _body = read_frontmatter(path)
        chain_id = fm.get("id") or path.stem
        chain_ids.add(chain_id)
        chain_uid = f"chain:{chain_id}"
        graph.add_node(
            chain_uid,
            ["Chain"],
            {
                "chain_id": chain_id,
                "name": fm.get("name"),
                "vm": fm.get("vm"),
                "consensus": fm.get("consensus"),
                "layer": fm.get("layer"),
                "sequencer": fm.get("sequencer"),
                "finality_slots": fm.get("finality_slots"),
                "finality_seconds": fm.get("finality_seconds"),
                "l1": fm.get("l1"),
                "native_bridge": fm.get("native_bridge"),
                "mev_infra": fm.get("mev_infra"),
                "defi_context": json.dumps(normalize_value(fm.get("defi_context", {})), ensure_ascii=False),
                "source_path": str(path.relative_to(risk_root)),
            },
        )
        risk_notes = fm.get("risk_notes") or {}
        for risk_id in fm.get("key_risks", []) or []:
            ensure_risk(graph, risk_id, known_risks, str(path.relative_to(risk_root)))
            graph.add_rel(
                chain_uid,
                "HAS_BASE_RISK",
                f"risk:{risk_id}",
                f"{chain_uid}:base_risk:{risk_id}",
                {
                    "note": risk_notes.get(risk_id),
                    "source_path": str(path.relative_to(risk_root)),
                },
            )
    return chain_ids


def add_protocols(
    graph: Graph,
    risk_root: Path,
    known_risks: set[str],
    protocol_slugs: set[str],
    chain_ids: set[str],
) -> None:
    for path in sorted((risk_root / "protocols").glob("*.md")):
        fm, _body = read_frontmatter(path)
        slug = fm.get("slug") or path.stem
        protocol_uid = f"protocol:{slug}"
        source_path = str(path.relative_to(risk_root))
        graph.add_node(
            protocol_uid,
            ["Protocol"],
            {
                "slug": slug,
                "name": fm.get("name"),
                "types": fm.get("types"),
                "audit_count": len(fm.get("audits") or []),
                "audits": json.dumps(normalize_value(fm.get("audits", [])), ensure_ascii=False),
                "source_path": source_path,
            },
        )

        for type_id in fm.get("types", []) or []:
            type_uid = f"type:{type_id}"
            graph.add_node(type_uid, ["ProtocolType"], {"type_id": type_id})
            graph.add_rel(
                protocol_uid,
                "HAS_TYPE",
                type_uid,
                f"{protocol_uid}:has_type:{type_id}",
                {"source_path": source_path},
            )

        deployments = fm.get("deployments", []) or []
        for deployment in deployments:
            chain = deployment.get("chain")
            if not chain:
                continue
            deployment_uid = f"deployment:{slug}.{chain}"
            graph.add_node(
                deployment_uid,
                ["Deployment"],
                {
                    "deployment_id": f"{slug}.{chain}",
                    "protocol_slug": slug,
                    "chain": chain,
                    "tvl_usd": deployment.get("tvl_usd"),
                    "since": deployment.get("since"),
                    "note": deployment.get("note"),
                    "source_path": source_path,
                },
            )
            graph.add_rel(
                protocol_uid,
                "HAS_DEPLOYMENT",
                deployment_uid,
                f"{protocol_uid}:deployment:{chain}",
                {"source_path": source_path},
            )
            chain_uid = f"chain:{chain}"
            graph.add_node(chain_uid, ["Chain"], {"chain_id": chain})
            graph.add_rel(
                deployment_uid,
                "DEPLOYED_ON",
                chain_uid,
                f"{deployment_uid}:deployed_on:{chain}",
                {"source_path": source_path},
            )

        for dep in fm.get("dependencies", []) or []:
            dep_id = dep.get("id")
            if not dep_id:
                continue
            dep_uid, dep_labels = dependency_target_uid(dep_id, protocol_slugs, chain_ids)
            dep_props: dict[str, Any] = {}
            if dep_uid.startswith("dependency:"):
                dep_props.update({"dependency_id": dep_id, "dependency_type": dep.get("type")})
            graph.add_node(dep_uid, dep_labels, dep_props)

            targets = rel_scope_targets(slug, deployments, dep.get("scope"))
            rel_props = {
                "dependency_id": dep_id,
                "dependency_type": dep.get("type"),
                "scope": dep.get("scope"),
                "assets": dep.get("assets"),
                "via": dep.get("via"),
                "note": dep.get("note"),
                "propagation_coeff": dep.get("propagation_coeff"),
                "confidence": dep.get("confidence"),
                "observed_at": dep.get("observed_at"),
                "source_path": source_path,
            }
            for target_uid in targets:
                graph.add_rel(
                    target_uid,
                    "DEPENDS_ON",
                    dep_uid,
                    f"{target_uid}:depends_on:{dep_id}",
                    rel_props,
                )
                for raw_asset in dep.get("assets", []) or []:
                    uid, labels, props = asset_uid(str(raw_asset))
                    props["source_path"] = source_path
                    graph.add_node(uid, labels, props)
                    graph.add_rel(
                        target_uid,
                        "USES_ASSET",
                        uid,
                        f"{target_uid}:uses_asset:{normalize_slug(str(raw_asset))}:{dep_id}",
                        {
                            "dependency_id": dep_id,
                            "dependency_type": dep.get("type"),
                            "scope": dep.get("scope"),
                            "source_path": source_path,
                        },
                    )

        for item in fm.get("active_risks", []) or []:
            risk_id = item.get("risk_id")
            if not risk_id:
                continue
            ensure_risk(graph, risk_id, known_risks, source_path)
            targets = risk_targets(slug, deployments, item.get("deployment"))
            severity_override = item.get("severity_override") or {}
            rel_props = {
                "risk_id": risk_id,
                "deployment": item.get("deployment"),
                "note": item.get("note") or severity_override.get("note"),
                "source_path": source_path,
            }
            rel_props.update(flatten_severity("override", severity_override))
            for target_uid in targets:
                graph.add_rel(
                    target_uid,
                    "HAS_ACTIVE_RISK",
                    f"risk:{risk_id}",
                    f"{target_uid}:active_risk:{risk_id}",
                    rel_props,
                )


def add_incidents(graph: Graph, risk_root: Path, known_risks: set[str], protocol_slugs: set[str]) -> None:
    incidents_dir = risk_root / "incidents"
    if not incidents_dir.is_dir():
        return
    for path in sorted(incidents_dir.glob("*.yaml")):
        if path.stem.startswith("bootstrap") or path.stem.startswith("README"):
            continue
        data = read_yaml(path)
        incident_uid = data.get("id")
        if not incident_uid:
            continue
        source_path = str(path.relative_to(risk_root))
        graph.add_node(
            incident_uid,
            ["Incident"],
            {
                "incident_id": incident_uid,
                "title": data.get("title"),
                "date": data.get("date"),
                "event_type": data.get("event_type"),
                "amount_lost_usd": data.get("amount_lost_usd"),
                "near_miss": data.get("near_miss"),
                "confidence": data.get("confidence"),
                "notes": data.get("notes"),
                "source_path": source_path,
                "source_urls": json.dumps(normalize_value(as_list(data.get("source_urls", []))), ensure_ascii=False),
                "risk_ids": json.dumps(normalize_value(as_list(data.get("risk_ids", []))), ensure_ascii=False),
                "chains": normalize_value(as_list(data.get("chains", []))),
                "affected_protocols": normalize_value(as_list(data.get("affected_protocols", []))),
                "affected_assets": normalize_value(as_list(data.get("affected_assets", []))),
            },
        )

        for risk_id in as_list(data.get("risk_ids", [])):
            ensure_risk(graph, risk_id, known_risks, source_path)
            graph.add_rel(
                incident_uid,
                "EVIDENCES_RISK",
                f"risk:{risk_id}",
                f"{incident_uid}:evidences:{risk_id}",
                {"source_path": source_path},
            )

        protocol_targets = list(as_list(data.get("affected_protocols", []))) + list(as_list(data.get("cascade_targets", [])))
        for protocol_slug in protocol_targets:
            if protocol_slug not in protocol_slugs:
                continue
            graph.add_rel(
                incident_uid,
                "INVOLVES_PROTOCOL",
                f"protocol:{protocol_slug}",
                f"{incident_uid}:involves_protocol:{protocol_slug}",
                {"source_path": source_path},
            )

        for chain_id in as_list(data.get("chains", [])):
            chain_uid = f"chain:{chain_id}"
            graph.add_node(chain_uid, ["Chain"], {"chain_id": chain_id})
            graph.add_rel(
                incident_uid,
                "INVOLVES_CHAIN",
                chain_uid,
                f"{incident_uid}:involves_chain:{chain_id}",
                {"source_path": source_path},
            )

        for raw_asset in as_list(data.get("affected_assets", [])):
            uid, labels, props = asset_uid(str(raw_asset))
            props["source_path"] = source_path
            graph.add_node(uid, labels, props)
            asset_slug = normalize_slug(str(raw_asset))
            graph.add_rel(
                incident_uid,
                "INVOLVES_ASSET",
                uid,
                f"{incident_uid}:involves_asset:{asset_slug}",
                {"source_path": source_path},
            )


def add_attack_patterns(graph: Graph, risk_root: Path, known_risks: set[str]) -> None:
    for path in sorted((risk_root / "attack_patterns").glob("*.yaml")):
        data = read_yaml(path)
        source_path = str(path.relative_to(risk_root))
        for pattern in data.get("patterns", []) or []:
            pattern_id = pattern.get("id")
            if not pattern_id:
                continue
            pattern_uid = f"attack_pattern:{pattern_id}"
            graph.add_node(
                pattern_uid,
                ["AttackPattern"],
                {
                    "pattern_id": pattern_id,
                    "name": pattern.get("name"),
                    "category": data.get("category"),
                    "observed": pattern.get("observed"),
                    "hops": pattern.get("hops"),
                    "observed_examples": pattern.get("observed_examples"),
                    "source_path": source_path,
                },
            )
            for risk_id in pattern.get("risk_ids", []) or []:
                ensure_risk(graph, risk_id, known_risks, source_path)
                graph.add_rel(
                    pattern_uid,
                    "INVOLVES_RISK",
                    f"risk:{risk_id}",
                    f"{pattern_uid}:risk:{risk_id}",
                    {"source_path": source_path},
                )


def add_markets(graph: Graph, risk_root: Path, chain_ids: set[str]) -> None:
    """Add Token and Market nodes from protocol_markets.json (built by build_protocol_markets.py)."""
    markets_path = risk_root / "neo4j" / "protocol_markets.json"
    if not markets_path.exists():
        return
    data: dict[str, list[dict]] = json.loads(markets_path.read_text(encoding="utf-8"))
    source_path = str(markets_path.relative_to(risk_root))

    for protocol_slug, pools in data.items():
        protocol_uid = f"protocol:{protocol_slug}"
        for pool in pools:
            pool_id = pool.get("pool_id") or ""
            if not pool_id:
                continue
            chain_raw = (pool.get("chain") or "").lower().replace(" ", "_")
            symbol = pool.get("symbol") or ""
            market_uid = f"market:{pool_id}"

            graph.add_node(
                market_uid,
                ["Market"],
                {
                    "market_id": pool_id,
                    "name": symbol or pool_id,
                    "protocol_slug": protocol_slug,
                    "chain": chain_raw,
                    "symbol": symbol,
                    "tvl_usd": pool.get("tvl_usd"),
                    "apy": pool.get("apy"),
                    "apy_base": pool.get("apy_base"),
                    "apy_reward": pool.get("apy_reward"),
                    "apy_mean_30d": pool.get("apy_mean_30d"),
                    "volume_usd_1d": pool.get("volume_usd_1d"),
                    "il_risk": pool.get("il_risk"),
                    "stablecoin": pool.get("stablecoin"),
                    "source_path": source_path,
                },
            )

            graph.add_rel(
                protocol_uid,
                "HAS_MARKET",
                market_uid,
                f"{protocol_uid}:has_market:{pool_id}",
                {"source_path": source_path},
            )

            # Market → Chain
            if chain_raw in chain_ids:
                graph.add_rel(
                    market_uid,
                    "ON_CHAIN",
                    f"chain:{chain_raw}",
                    f"{market_uid}:on_chain:{chain_raw}",
                    {"source_path": source_path},
                )

            # Market → Token (one per underlying token with resolved symbol)
            token_symbols: list = pool.get("token_symbols") or []
            underlying: list = pool.get("underlying_tokens") or []
            for i, sym in enumerate(token_symbols):
                if not sym:
                    # Fall back to address prefix for unknown tokens
                    addr = underlying[i] if i < len(underlying) else None
                    if addr:
                        sym = f"unknown:{addr[:8]}"
                    else:
                        continue
                asset_uid_str, asset_labels, asset_props = asset_uid(sym)
                asset_props["source_path"] = source_path
                graph.add_node(asset_uid_str, asset_labels, asset_props)
                graph.add_rel(
                    market_uid,
                    "USES_ASSET",
                    asset_uid_str,
                    f"{market_uid}:uses_asset:{sym.upper()}:{i}",
                    {"source_path": source_path},
                )


def collect_protocol_slugs(risk_root: Path) -> set[str]:
    slugs = set()
    for path in sorted((risk_root / "protocols").glob("*.md")):
        fm, _body = read_frontmatter(path)
        slugs.add(fm.get("slug") or path.stem)
    return slugs


def write_cypher(graph: Graph, risk_root: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    constraints_path = risk_root / "neo4j" / "constraints.cypher"
    lines = [
        "// Generated by risk_model/neo4j/import_risk_model.py",
        "// Do not edit by hand; update source files and regenerate.",
        "",
    ]
    if constraints_path.exists():
        lines.extend(constraints_path.read_text(encoding="utf-8").strip().splitlines())
        lines.append("")

    for node in sorted(graph.nodes.values(), key=lambda item: item.uid):
        labels = labels_literal(node.labels)
        props = props_literal(node.props)
        lines.append(f"MERGE (n{labels} {{uid: {cypher_literal(node.uid)}}})")
        lines.append(f"SET n += {props};")
        lines.append("")

    for rel in sorted(graph.relationships.values(), key=lambda item: item.uid):
        props = props_literal(rel.props)
        lines.append(
            f"MATCH (a:RiskModelNode {{uid: {cypher_literal(rel.source_uid)}}}), "
            f"(b:RiskModelNode {{uid: {cypher_literal(rel.target_uid)}}})"
        )
        lines.append(f"MERGE (a)-[r:{rel.rel_type} {{uid: {cypher_literal(rel.uid)}}}]->(b)")
        lines.append(f"SET r += {props};")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def build_graph(risk_root: Path) -> Graph:
    graph = Graph()
    known_risks = add_taxonomy(graph, risk_root)
    add_detailed_risks(graph, risk_root)
    add_types(graph, risk_root, known_risks)
    chain_ids = add_chains(graph, risk_root, known_risks)
    protocol_slugs = collect_protocol_slugs(risk_root)
    add_protocols(graph, risk_root, known_risks, protocol_slugs, chain_ids)
    add_attack_patterns(graph, risk_root, known_risks)
    add_incidents(graph, risk_root, known_risks, protocol_slugs)
    add_markets(graph, risk_root, chain_ids)
    return graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Neo4j Cypher import for risk_model.")
    parser.add_argument("--risk-root", type=Path, default=RISK_ROOT, help="Path to risk_model directory")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output .cypher path")
    args = parser.parse_args()

    graph = build_graph(args.risk_root)
    write_cypher(graph, args.risk_root, args.out)

    print(f"wrote {args.out}")
    print(f"nodes: {len(graph.nodes)}")
    print(f"relationships: {len(graph.relationships)}")
    if graph.warnings:
        print(f"warnings: {len(graph.warnings)}", file=sys.stderr)
        for warning in graph.warnings[:50]:
            print(f"- {warning}", file=sys.stderr)
        if len(graph.warnings) > 50:
            print(f"- ... {len(graph.warnings) - 50} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
