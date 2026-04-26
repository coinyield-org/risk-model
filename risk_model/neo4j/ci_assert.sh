#!/usr/bin/env bash
set -euo pipefail

COMPOSE="${COMPOSE:-docker compose}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-password}"

read -r -a compose_cmd <<< "$COMPOSE"

run_scalar() {
  local query="$1"
  "${compose_cmd[@]}" exec -T neo4j cypher-shell \
    -u "$NEO4J_USER" \
    -p "$NEO4J_PASSWORD" \
    --format plain \
    "$query" | tail -n 1 | tr -d '\r'
}

failures=0

assert_zero() {
  local name="$1"
  local query="$2"
  local value
  value="$(run_scalar "$query")"
  echo "$name=$value"
  if [[ "$value" != "0" ]]; then
    echo "FAIL: $name must be 0" >&2
    failures=1
  fi
}

assert_positive() {
  local name="$1"
  local query="$2"
  local value
  value="$(run_scalar "$query")"
  echo "$name=$value"
  if [[ "${value:-0}" -le 0 ]]; then
    echo "FAIL: $name must be > 0" >&2
    failures=1
  fi
}

assert_positive "risk_model_nodes" "MATCH (n:RiskModelNode) RETURN count(n) AS value;"
assert_positive "relationships" "MATCH ()-[r]->() RETURN count(r) AS value;"
assert_zero "unknown_risk_ids" "MATCH (r:Risk) WHERE coalesce(r.taxonomy_defined, false) = false RETURN count(r) AS value;"
assert_zero "deployments_without_exactly_one_chain" "MATCH (d:Deployment) OPTIONAL MATCH (d)-[:DEPLOYED_ON]->(c:Chain) WITH d, count(c) AS chain_count WHERE chain_count <> 1 RETURN count(d) AS value;"
assert_zero "deployments_without_exactly_one_parent_protocol" "MATCH (d:Deployment) OPTIONAL MATCH (:Protocol)-[:HAS_DEPLOYMENT]->(d) WITH d, count(*) AS protocol_count WHERE protocol_count <> 1 RETURN count(d) AS value;"
assert_zero "relationships_without_source_path" "MATCH ()-[r]->() WHERE r.source_path IS NULL OR trim(r.source_path) = '' RETURN count(r) AS value;"
assert_zero "chains_without_source_path" "MATCH (c:Chain) WHERE c.source_path IS NULL OR trim(c.source_path) = '' RETURN count(c) AS value;"

if [[ "$failures" -ne 0 ]]; then
  exit 1
fi

echo "CI integrity checks passed."
