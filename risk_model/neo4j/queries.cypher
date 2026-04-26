// 1. Blast radius: what depends on Lido directly or indirectly?
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected:RiskModelNode)
RETURN affected.uid AS affected, [n IN nodes(path) | n.uid] AS path
ORDER BY size(path), affected
LIMIT 100;

// 2. Blast radius for an external dependency such as Chainlink.
MATCH path = (:ExternalDependency {dependency_id: "chainlink"})<-[:DEPENDS_ON*1..4]-(affected:RiskModelNode)
RETURN affected.uid AS affected, [n IN nodes(path) | n.uid] AS path
ORDER BY size(path), affected
LIMIT 100;

// 3. All active uses of a risk id.
MATCH (holder:RiskModelNode)-[rel:HAS_ACTIVE_RISK]->(:Risk {risk_id: "oracle_staleness"})
RETURN holder.uid AS holder, labels(holder) AS labels, rel.deployment AS deployment, rel.note AS note
ORDER BY holder;

// 4. Shared dependency concentration: deployments that depend on both Circle and Chainlink.
MATCH (d:Deployment)-[:DEPENDS_ON]->(:ExternalDependency {dependency_id: "circle"})
MATCH (d)-[:DEPENDS_ON]->(:ExternalDependency {dependency_id: "chainlink"})
RETURN d.uid AS deployment, d.tvl_usd AS tvl_usd
ORDER BY tvl_usd DESC;

// 5. Weighted upstream propagation using propagation_coeff when present.
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected:RiskModelNode)
WITH affected, path,
     reduce(coeff = 1.0, r IN relationships(path) | coeff * coalesce(r.propagation_coeff, 1.0)) AS propagated
RETURN affected.uid AS affected, propagated, [n IN nodes(path) | n.uid] AS path
ORDER BY propagated DESC, affected
LIMIT 100;

// 6. Find dependency fan-in: external dependencies with the most direct consumers.
MATCH (consumer:RiskModelNode)-[:DEPENDS_ON]->(dep:ExternalDependency)
RETURN dep.dependency_id AS dependency, dep.dependency_type AS type, count(DISTINCT consumer) AS consumers
ORDER BY consumers DESC, dependency
LIMIT 50;

// 7. Find protocols with deepest dependency chains.
MATCH path = (p:Protocol)-[:HAS_DEPLOYMENT]->(:Deployment)-[:DEPENDS_ON*1..5]->(upstream)
RETURN p.slug AS protocol, max(length(path)) AS max_depth, count(path) AS paths
ORDER BY max_depth DESC, paths DESC
LIMIT 50;

// 8. Incidents evidencing a risk (latest 5).
MATCH (i:Incident)-[:EVIDENCES_RISK]->(:Risk {risk_id: "oracle_staleness"})
RETURN i.incident_id AS id, i.date AS date, i.title AS title, i.amount_lost_usd AS loss_usd
ORDER BY i.date DESC
LIMIT 5;

// 9. Risk calibration: risk_ids with most incident evidence (for likelihood scoring).
MATCH (i:Incident)-[:EVIDENCES_RISK]->(r:Risk)
RETURN r.risk_id AS risk_id, count(i) AS incident_count, sum(i.amount_lost_usd) AS total_loss_usd
ORDER BY incident_count DESC, total_loss_usd DESC
LIMIT 50;

// 10. Blast radius combined with incident evidence.
MATCH (i:Incident)-[:INVOLVES_PROTOCOL]->(p:Protocol)<-[:DEPENDS_ON*1..3]-(dep)
RETURN p.slug AS epicenter, count(DISTINCT i) AS incidents, count(DISTINCT dep) AS downstream_protocols
ORDER BY incidents DESC, downstream_protocols DESC
LIMIT 20;

// 11. Kelp / rsETH blast radius: what may be affected if Kelp's rsETH is compromised?
// This combines three currently modeled signals:
// - direct dependency on protocol:kelp;
// - explicit use of asset:rseth;
// - dependency edges whose assets/via fields already mention rsETH or kelp.
CALL {
  MATCH path = (:Protocol {slug: "kelp"})<-[:DEPENDS_ON*1..3]-(affected:RiskModelNode)
  OPTIONAL MATCH (p:Protocol)-[:HAS_DEPLOYMENT]->(affected)
  RETURN
    affected.uid AS affected,
    labels(affected) AS labels,
    coalesce(p.slug, CASE WHEN "Protocol" IN labels(affected) THEN affected.slug ELSE null END) AS protocol,
    CASE WHEN "Deployment" IN labels(affected) THEN affected.chain ELSE null END AS chain,
    CASE WHEN "Deployment" IN labels(affected) THEN affected.tvl_usd ELSE null END AS tvl_usd,
    "direct_depends_on_protocol_kelp" AS exposure_signal,
    [n IN nodes(path) | n.uid] AS path

  UNION

  MATCH (affected:RiskModelNode)-[:USES_ASSET]->(:Asset {asset_id: "rseth"})
  OPTIONAL MATCH (p:Protocol)-[:HAS_DEPLOYMENT]->(affected)
  RETURN
    affected.uid AS affected,
    labels(affected) AS labels,
    coalesce(p.slug, CASE WHEN "Protocol" IN labels(affected) THEN affected.slug ELSE null END) AS protocol,
    CASE WHEN "Deployment" IN labels(affected) THEN affected.chain ELSE null END AS chain,
    CASE WHEN "Deployment" IN labels(affected) THEN affected.tvl_usd ELSE null END AS tvl_usd,
    "uses_asset_rseth" AS exposure_signal,
    [affected.uid, "asset:rseth"] AS path

  UNION

  MATCH (affected:Deployment)-[r:DEPENDS_ON]->(upstream:RiskModelNode)
  WHERE "kelp" IN coalesce(r.via, [])
     OR any(asset IN coalesce(r.assets, []) WHERE toLower(toString(asset)) CONTAINS "rseth")
  OPTIONAL MATCH (p:Protocol)-[:HAS_DEPLOYMENT]->(affected)
  RETURN
    affected.uid AS affected,
    labels(affected) AS labels,
    p.slug AS protocol,
    affected.chain AS chain,
    affected.tvl_usd AS tvl_usd,
    "dependency_edge_mentions_kelp_or_rseth" AS exposure_signal,
    [affected.uid, upstream.uid] AS path
}
RETURN DISTINCT affected, labels, protocol, chain, tvl_usd, exposure_signal, path
ORDER BY coalesce(tvl_usd, 0) DESC, affected;
