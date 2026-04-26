// Risk graph verification and diagnostic queries.
//
// Run from the repo root:
//   make neo4j-check
//
// Or paste individual queries into Neo4j Browser.
//
// These checks are intentionally a mix of:
// - smoke checks that should pass on every import;
// - integrity checks that reveal modeling gaps;
// - heavier graph diagnostics for cascade reasoning.

// ---------------------------------------------------------------------------
// 1. Smoke: graph is non-empty.
// ---------------------------------------------------------------------------
CALL {
  MATCH (n:RiskModelNode) RETURN count(n) AS nodes
}
CALL {
  MATCH ()-[r]->() RETURN count(r) AS relationships
}
RETURN
  "graph_non_empty" AS check,
  CASE WHEN nodes > 0 AND relationships > 0 THEN "PASS" ELSE "FAIL" END AS status,
  nodes,
  relationships;

// ---------------------------------------------------------------------------
// 2. Smoke: expected core labels are present.
// ---------------------------------------------------------------------------
CALL {
  MATCH (n:Protocol) RETURN count(n) AS protocols
}
CALL {
  MATCH (n:Deployment) RETURN count(n) AS deployments
}
CALL {
  MATCH (n:Chain) RETURN count(n) AS chains
}
CALL {
  MATCH (n:Risk) RETURN count(n) AS risks
}
RETURN
  "core_label_counts" AS check,
  CASE
    WHEN protocols >= 90 AND deployments >= 100 AND chains >= 8 AND risks >= 100
    THEN "PASS"
    ELSE "REVIEW"
  END AS status,
  protocols,
  deployments,
  chains,
  risks;

// ---------------------------------------------------------------------------
// 3. Distribution: node counts by label.
// ---------------------------------------------------------------------------
MATCH (n:RiskModelNode)
UNWIND labels(n) AS label
RETURN label, count(*) AS nodes
ORDER BY nodes DESC, label;

// ---------------------------------------------------------------------------
// 4. Distribution: relationship counts by type.
// ---------------------------------------------------------------------------
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS relationships
ORDER BY relationships DESC, relationship_type;

// ---------------------------------------------------------------------------
// 5. Integrity: every RiskModelNode should have a uid.
// ---------------------------------------------------------------------------
MATCH (n:RiskModelNode)
WHERE n.uid IS NULL OR trim(n.uid) = ""
RETURN
  "missing_node_uid" AS check,
  CASE WHEN count(n) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(n) AS bad_nodes,
  collect(labels(n))[0..20] AS examples;

// ---------------------------------------------------------------------------
// 6. Integrity: importer should not create unknown risk IDs.
// ---------------------------------------------------------------------------
MATCH (r:Risk)
WHERE coalesce(r.taxonomy_defined, false) = false
RETURN
  "unknown_risk_ids" AS check,
  CASE WHEN count(r) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(r) AS unknown_risks,
  collect(r.risk_id)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 7. Integrity: active risk edges should point to taxonomy-defined risks.
// ---------------------------------------------------------------------------
MATCH (holder:RiskModelNode)-[:HAS_ACTIVE_RISK]->(risk:Risk)
WHERE coalesce(risk.taxonomy_defined, false) = false
RETURN
  "active_edges_to_unknown_risks" AS check,
  CASE WHEN count(risk) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(risk) AS bad_edges,
  collect(DISTINCT holder.uid + " -> " + risk.risk_id)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 8. Integrity: every deployment should link to exactly one chain.
// ---------------------------------------------------------------------------
MATCH (d:Deployment)
OPTIONAL MATCH (d)-[:DEPLOYED_ON]->(c:Chain)
WITH d, count(c) AS chain_count
WHERE chain_count <> 1
RETURN
  "deployment_chain_link" AS check,
  CASE WHEN count(d) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(d) AS bad_deployments,
  collect(d.uid)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 9. Integrity: every deployment should have a parent protocol.
// ---------------------------------------------------------------------------
MATCH (d:Deployment)
OPTIONAL MATCH (p:Protocol)-[:HAS_DEPLOYMENT]->(d)
WITH d, count(p) AS protocol_count
WHERE protocol_count <> 1
RETURN
  "deployment_parent_protocol" AS check,
  CASE WHEN count(d) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(d) AS bad_deployments,
  collect(d.uid)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 10. Integrity: relationships should retain source_path for traceability.
// ---------------------------------------------------------------------------
MATCH ()-[r]->()
WHERE r.source_path IS NULL OR trim(r.source_path) = ""
RETURN
  "relationship_source_path" AS check,
  CASE WHEN count(r) = 0 THEN "PASS" ELSE "FAIL" END AS status,
  count(r) AS relationships_without_source,
  collect(type(r))[0..50] AS example_relationship_types;

// ---------------------------------------------------------------------------
// 11. Modeling coverage: dependency edge metadata coverage.
// This is not expected to pass yet; it shows how far the graph is from
// exposure-weighted cascade scoring.
// ---------------------------------------------------------------------------
MATCH ()-[r:DEPENDS_ON]->()
RETURN
  "depends_on_metadata_coverage" AS check,
  "INFO" AS status,
  count(r) AS total_depends_on,
  count(r.propagation_coeff) AS with_propagation_coeff,
  count(r.confidence) AS with_confidence,
  count(r.observed_at) AS with_observed_at,
  count(r.assets) AS with_assets,
  count(r.via) AS with_via;

// ---------------------------------------------------------------------------
// 12. Modeling coverage: active risks without notes.
// ---------------------------------------------------------------------------
MATCH (holder:RiskModelNode)-[r:HAS_ACTIVE_RISK]->(risk:Risk)
WHERE r.note IS NULL OR trim(r.note) = ""
RETURN
  "active_risks_without_note" AS check,
  CASE WHEN count(r) = 0 THEN "PASS" ELSE "REVIEW" END AS status,
  count(r) AS edges_without_note,
  collect(holder.uid + " -> " + risk.risk_id)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 13. Protocol risk coverage: protocols with no active risk directly or on any
// deployment.
// ---------------------------------------------------------------------------
MATCH (p:Protocol)
WHERE NOT (p)-[:HAS_ACTIVE_RISK]->(:Risk)
  AND NOT EXISTS {
    MATCH (p)-[:HAS_DEPLOYMENT]->(:Deployment)-[:HAS_ACTIVE_RISK]->(:Risk)
  }
RETURN
  "protocols_without_active_risks" AS check,
  CASE WHEN count(p) = 0 THEN "PASS" ELSE "REVIEW" END AS status,
  count(p) AS protocols_without_active_risks,
  collect(p.slug)[0..50] AS examples;

// ---------------------------------------------------------------------------
// 14. Dependency concentration: external dependencies with the largest fan-in.
// ---------------------------------------------------------------------------
MATCH (consumer:RiskModelNode)-[:DEPENDS_ON]->(dep:ExternalDependency)
RETURN
  dep.dependency_id AS dependency,
  dep.dependency_type AS dependency_type,
  count(DISTINCT consumer) AS direct_consumers,
  collect(DISTINCT consumer.uid)[0..20] AS example_consumers
ORDER BY direct_consumers DESC, dependency
LIMIT 50;

// ---------------------------------------------------------------------------
// 15. Dependency concentration: protocols with the largest deployment TVL tied
// to an external dependency.
// ---------------------------------------------------------------------------
MATCH (d:Deployment)-[:DEPENDS_ON]->(dep:ExternalDependency)
WITH dep, count(DISTINCT d) AS deployments, sum(coalesce(d.tvl_usd, 0)) AS dependent_tvl_usd
RETURN
  dep.dependency_id AS dependency,
  dep.dependency_type AS dependency_type,
  deployments,
  dependent_tvl_usd
ORDER BY dependent_tvl_usd DESC, deployments DESC
LIMIT 50;

// ---------------------------------------------------------------------------
// 16. Risk concentration: most common active risks.
// ---------------------------------------------------------------------------
MATCH (holder:RiskModelNode)-[:HAS_ACTIVE_RISK]->(risk:Risk)
RETURN
  risk.risk_id AS risk_id,
  risk.category_id AS category_id,
  count(DISTINCT holder) AS holders,
  collect(DISTINCT holder.uid)[0..20] AS example_holders
ORDER BY holders DESC, risk_id
LIMIT 50;

// ---------------------------------------------------------------------------
// 17. Risk lookup example: latest usable view for bad_debt_socialization.
// Incident nodes are not implemented yet, so this currently lists holders.
// ---------------------------------------------------------------------------
MATCH (holder:RiskModelNode)-[r:HAS_ACTIVE_RISK]->(:Risk {risk_id: "bad_debt_socialization"})
RETURN
  holder.uid AS holder,
  labels(holder) AS labels,
  r.deployment AS deployment,
  r.note AS note,
  r.source_path AS source_path
ORDER BY holder
LIMIT 100;

// ---------------------------------------------------------------------------
// 18. Future incident layer check: should be 0 until incidents are implemented.
// ---------------------------------------------------------------------------
MATCH (i:Incident)
RETURN
  "incident_layer_present" AS check,
  CASE WHEN count(i) > 0 THEN "PASS" ELSE "TODO" END AS status,
  count(i) AS incident_nodes;

// ---------------------------------------------------------------------------
// 19. Future incident query shape: latest 5 incidents for oracle_staleness.
// This returns no rows until Incident nodes are implemented.
// ---------------------------------------------------------------------------
MATCH (:Risk {risk_id: "oracle_staleness"})<-[:EVIDENCES_RISK]-(i:Incident)
RETURN
  i.date AS date,
  i.title AS title,
  i.amount_lost_usd AS amount_lost_usd,
  i.source_urls AS source_urls
ORDER BY i.date DESC
LIMIT 5;

// ---------------------------------------------------------------------------
// 20. Blast radius: what directly or indirectly depends on Lido?
// ---------------------------------------------------------------------------
MATCH path = (:Protocol {slug: "lido"})<-[:DEPENDS_ON*1..4]-(affected:RiskModelNode)
RETURN
  affected.uid AS affected,
  labels(affected) AS labels,
  length(path) AS hops,
  [n IN nodes(path) | n.uid] AS path_nodes
ORDER BY hops, affected
LIMIT 100;

// ---------------------------------------------------------------------------
// 21. Blast radius: what directly or indirectly depends on Chainlink?
// ---------------------------------------------------------------------------
MATCH path = (:ExternalDependency {dependency_id: "chainlink"})<-[:DEPENDS_ON*1..4]-(affected:RiskModelNode)
RETURN
  affected.uid AS affected,
  labels(affected) AS labels,
  length(path) AS hops,
  [n IN nodes(path) | n.uid] AS path_nodes
ORDER BY hops, affected
LIMIT 100;

// ---------------------------------------------------------------------------
// 22. Aave V3 deployment comparison by chain.
// ---------------------------------------------------------------------------
MATCH (:Protocol {slug: "aave_v3"})-[:HAS_DEPLOYMENT]->(d:Deployment)
OPTIONAL MATCH (d)-[:HAS_ACTIVE_RISK]->(risk:Risk)
WITH d, collect(DISTINCT risk.risk_id) AS active_risks
OPTIONAL MATCH (d)-[:DEPENDS_ON]->(dep:RiskModelNode)
WITH d, active_risks, collect(DISTINCT dep.uid) AS dependencies
RETURN
  d.chain AS chain,
  d.tvl_usd AS tvl_usd,
  active_risks,
  dependencies
ORDER BY tvl_usd DESC;

// ---------------------------------------------------------------------------
// 23. Aave / Kelp / rsETH diagnostic.
// This exposes the current limitation: Kelp may appear as a via-property or
// rsETH asset reference, not yet as a first-class market edge.
// ---------------------------------------------------------------------------
MATCH (:Protocol {slug: "aave_v3"})-[:HAS_DEPLOYMENT]->(d:Deployment)-[r:DEPENDS_ON]->(dep:RiskModelNode)
WHERE "kelp" IN coalesce(r.via, [])
   OR any(asset IN coalesce(r.assets, []) WHERE toLower(toString(asset)) CONTAINS "rseth")
RETURN
  d.uid AS aave_deployment,
  dep.uid AS upstream_dependency,
  r.dependency_type AS dependency_type,
  r.scope AS scope,
  r.assets AS assets,
  r.via AS via,
  r.source_path AS source_path
ORDER BY aave_deployment, upstream_dependency;

// ---------------------------------------------------------------------------
// 24. Kelp active risk surface by deployment.
// ---------------------------------------------------------------------------
MATCH (:Protocol {slug: "kelp"})-[:HAS_DEPLOYMENT]->(d:Deployment)
OPTIONAL MATCH (d)-[r:HAS_ACTIVE_RISK]->(risk:Risk)
RETURN
  d.uid AS kelp_deployment,
  d.chain AS chain,
  d.tvl_usd AS tvl_usd,
  collect(DISTINCT {
    risk_id: risk.risk_id,
    category_id: risk.category_id,
    note: r.note
  }) AS active_risks
ORDER BY tvl_usd DESC;

// ---------------------------------------------------------------------------
// 25. Recursive dependency chains: deepest chains currently represented.
// ---------------------------------------------------------------------------
MATCH path = (p:Protocol)-[:HAS_DEPLOYMENT]->(:Deployment)-[:DEPENDS_ON*1..5]->(upstream:RiskModelNode)
RETURN
  p.slug AS protocol,
  upstream.uid AS upstream,
  length(path) AS hops,
  [n IN nodes(path) | n.uid] AS path_nodes
ORDER BY hops DESC, protocol, upstream
LIMIT 100;

// ---------------------------------------------------------------------------
// 26. Potential dependency cycles. A non-empty result is not automatically a
// bug, but it should be reviewed because feedback loops matter for cascades.
// ---------------------------------------------------------------------------
MATCH path = (n:RiskModelNode)-[:DEPENDS_ON*2..6]->(n)
RETURN
  n.uid AS cycle_node,
  length(path) AS hops,
  [x IN nodes(path) | x.uid] AS path_nodes
ORDER BY hops DESC, cycle_node
LIMIT 50;

// ---------------------------------------------------------------------------
// 27. Shared dependency pairs across deployments.
// Useful for finding correlated failure domains.
// ---------------------------------------------------------------------------
MATCH (d:Deployment)-[:DEPENDS_ON]->(a:RiskModelNode)
MATCH (d)-[:DEPENDS_ON]->(b:RiskModelNode)
WHERE a.uid < b.uid
WITH a, b, count(DISTINCT d) AS shared_deployments, sum(coalesce(d.tvl_usd, 0)) AS shared_tvl_usd
WHERE shared_deployments >= 2
RETURN
  a.uid AS dependency_a,
  b.uid AS dependency_b,
  shared_deployments,
  shared_tvl_usd
ORDER BY shared_tvl_usd DESC, shared_deployments DESC
LIMIT 100;

// ---------------------------------------------------------------------------
// 28. Assets and price pairs inferred from dependency fields.
// ---------------------------------------------------------------------------
MATCH (consumer:RiskModelNode)-[:USES_ASSET]->(asset:RiskModelNode)
RETURN
  asset.uid AS asset,
  labels(asset) AS labels,
  count(DISTINCT consumer) AS consumers,
  collect(DISTINCT consumer.uid)[0..20] AS example_consumers
ORDER BY consumers DESC, asset
LIMIT 100;

// ---------------------------------------------------------------------------
// 29. Protocols with highest explicit deployment TVL.
// ---------------------------------------------------------------------------
MATCH (p:Protocol)-[:HAS_DEPLOYMENT]->(d:Deployment)
WITH p, sum(coalesce(d.tvl_usd, 0)) AS explicit_tvl_usd, count(d) AS deployments
RETURN p.slug AS protocol, deployments, explicit_tvl_usd
ORDER BY explicit_tvl_usd DESC
LIMIT 50;

// ---------------------------------------------------------------------------
// 30. Risk category coverage.
// ---------------------------------------------------------------------------
MATCH (risk:Risk)-[:IN_CATEGORY]->(category:RiskCategory)
RETURN
  category.category_id AS category_id,
  category.name AS name,
  count(risk) AS risks
ORDER BY risks DESC, category_id;

// ---------------------------------------------------------------------------
// 31. Smoke: Incident nodes are present after bootstrap.
// ---------------------------------------------------------------------------
MATCH (i:Incident)
RETURN
  "incident_count" AS check,
  CASE WHEN count(i) > 0 THEN "PASS" ELSE "WARN" END AS status,
  count(i) AS incidents;

// ---------------------------------------------------------------------------
// 32. Coverage: reviewed incidents should have at least one EVIDENCES_RISK edge.
// Auto-generated low-confidence files may intentionally have risk_ids: [] until
// manual review, so this is a review queue rather than a hard failure.
// ---------------------------------------------------------------------------
MATCH (i:Incident)
WHERE NOT (i)-[:EVIDENCES_RISK]->()
RETURN
  "incident_missing_risk_link" AS check,
  CASE WHEN count(i) = 0 THEN "PASS" ELSE "REVIEW" END AS status,
  count(i) AS bad_incidents,
  collect(i.incident_id)[0..10] AS examples;
