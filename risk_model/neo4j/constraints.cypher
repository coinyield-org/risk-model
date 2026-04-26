CREATE CONSTRAINT risk_model_node_uid IF NOT EXISTS
FOR (n:RiskModelNode)
REQUIRE n.uid IS UNIQUE;

CREATE INDEX protocol_slug IF NOT EXISTS
FOR (n:Protocol)
ON (n.slug);

CREATE INDEX deployment_protocol_chain IF NOT EXISTS
FOR (n:Deployment)
ON (n.protocol_slug, n.chain);

CREATE INDEX chain_id IF NOT EXISTS
FOR (n:Chain)
ON (n.chain_id);

CREATE INDEX risk_id IF NOT EXISTS
FOR (n:Risk)
ON (n.risk_id);

CREATE INDEX external_dependency_id IF NOT EXISTS
FOR (n:ExternalDependency)
ON (n.dependency_id);

CREATE INDEX incident_id IF NOT EXISTS
FOR (n:Incident)
ON (n.incident_id);
