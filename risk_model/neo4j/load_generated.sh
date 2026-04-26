#!/usr/bin/env bash
set -euo pipefail

COMPOSE="${COMPOSE:-docker compose}"
NEO4J_USER="${NEO4J_USER:-neo4j}"
NEO4J_PASSWORD="${NEO4J_PASSWORD:-password}"
CYPHER_FILE="${1:-risk_model/neo4j/generated/risk_model.cypher}"

if [[ ! -f "$CYPHER_FILE" ]]; then
  echo "Cypher file not found: $CYPHER_FILE" >&2
  exit 1
fi

read -r -a compose_cmd <<< "$COMPOSE"

echo "Waiting for Neo4j to accept Cypher connections..."
for _ in $(seq 1 60); do
  if "${compose_cmd[@]}" exec -T neo4j cypher-shell \
    -u "$NEO4J_USER" \
    -p "$NEO4J_PASSWORD" \
    "RETURN 1;" >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

"${compose_cmd[@]}" exec -T neo4j cypher-shell \
  -u "$NEO4J_USER" \
  -p "$NEO4J_PASSWORD" < "$CYPHER_FILE"

echo "Loaded $CYPHER_FILE into Neo4j."
