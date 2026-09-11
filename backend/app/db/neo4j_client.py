from typing import Any, Dict, List, Optional

# Cypher DDL Constraints for KavachNet Knowledge Graph
CYPHER_CONSTRAINTS = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (ph:Phone) REQUIRE ph.id IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.id IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (b:BankAccount) REQUIRE b.id IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE;"
]

# Cypher Insert Templates
CYPHER_UPSERT_PERSON = """
MERGE (p:Person {id: $id})
SET p.label = $label,
    p.sub_role = $sub_role,
    p.centrality_score = $centrality_score,
    p.risk_level = $risk_level,
    p.case_id = $case_id,
    p.updated_at = datetime()
RETURN p;
"""

CYPHER_UPSERT_EDGE = """
MATCH (source {id: $source_id})
MATCH (target {id: $target_id})
MERGE (source)-[r:INTERACTS_WITH {id: $edge_id}]->(target)
SET r.type = $type,
    r.label = $label,
    r.confidence = $confidence,
    r.confidence_explanation = $confidence_explanation,
    r.category = $category,
    r.interaction_count = $interaction_count
RETURN r;
"""

CYPHER_FETCH_CASE_GRAPH = """
MATCH (n {case_id: $case_id})
OPTIONAL MATCH (n)-[r]->(m {case_id: $case_id})
RETURN collect(DISTINCT n) as nodes, collect(DISTINCT r) as edges;
"""

class Neo4jGraphClient:
    """
    Neo4j Graph Client for KavachNet.
    Provides Cypher execution with graceful fallback for local development.
    """
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "kavachnet2026"):
        self.uri = uri
        self.user = user
        self.password = password
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    def get_ddl_statements(self) -> List[str]:
        """Returns all required Cypher schema constraint statements."""
        return CYPHER_CONSTRAINTS

    def format_for_cytoscape(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Converts raw Neo4j node/edge record dictionaries into Cytoscape.js format."""
        cytoscape_nodes = [{"data": n} for n in nodes]
        cytoscape_edges = [{"data": e} for e in edges]
        return {
            "elements": {
                "nodes": cytoscape_nodes,
                "edges": cytoscape_edges
            }
        }

neo4j_client = Neo4jGraphClient()
