ifneq (,$(wildcard .env))
include .env
export
endif

PYTHON ?= python3
COMPOSE ?= docker compose
NEO4J_USER ?= neo4j
NEO4J_PASSWORD ?= password
RISK_GRAPH_CYPHER ?= risk_model/neo4j/generated/risk_model.cypher
RISK_GRAPH_CHECKS ?= risk_model/neo4j/checks.cypher

.PHONY: risk-graph-build neo4j-up neo4j-down neo4j-logs neo4j-import neo4j-check neo4j-ci-check neo4j-clear neo4j-reset neo4j-shell

risk-graph-build:
	$(PYTHON) risk_model/neo4j/import_risk_model.py

neo4j-up:
	$(COMPOSE) up -d neo4j

neo4j-down:
	$(COMPOSE) down

neo4j-logs:
	$(COMPOSE) logs -f neo4j

neo4j-import: risk-graph-build
	bash risk_model/neo4j/load_generated.sh $(RISK_GRAPH_CYPHER)

neo4j-check:
	$(COMPOSE) exec -T neo4j cypher-shell -u $(NEO4J_USER) -p $(NEO4J_PASSWORD) < $(RISK_GRAPH_CHECKS)

neo4j-ci-check:
	bash risk_model/neo4j/ci_assert.sh

neo4j-clear:
	$(COMPOSE) exec -T neo4j cypher-shell -u $(NEO4J_USER) -p $(NEO4J_PASSWORD) "MATCH (n) DETACH DELETE n;"

neo4j-reset: neo4j-clear neo4j-import

neo4j-shell:
	$(COMPOSE) exec neo4j cypher-shell -u $(NEO4J_USER) -p $(NEO4J_PASSWORD)
