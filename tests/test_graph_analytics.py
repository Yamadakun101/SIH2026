"""
Unit Tests for Graph Analytics, Centrality Metrics, and Community Detection
"""

import json
import os
import unittest
from graph.graph_builder import CrimeGraph
from graph.centrality_analytics import CentralityAnalytics
from graph.syndicate_clustering import SyndicateClustering


class TestGraphAnalytics(unittest.TestCase):

    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data", "dl-2026-0412.json")
        self.graph = CrimeGraph.from_case_json(self.data_path)
        self.analytics = CentralityAnalytics(self.graph)
        self.clustering = SyndicateClustering(self.graph)

    def test_graph_loading_and_cytoscape_export(self):
        self.assertGreaterEqual(len(self.graph.nodes), 10)
        self.assertGreaterEqual(len(self.graph.edges), 9)

        cytoscape_json = self.graph.to_cytoscape_json()
        self.assertIn("case_id", cytoscape_json)
        self.assertIn("elements", cytoscape_json)
        self.assertIn("nodes", cytoscape_json["elements"])
        self.assertIn("edges", cytoscape_json["elements"])

        # Validate node element structure
        first_node = cytoscape_json["elements"]["nodes"][0]
        self.assertIn("data", first_node)
        self.assertIn("id", first_node["data"])
        self.assertIn("label", first_node["data"])
        self.assertIn("type", first_node["data"])

    def test_centrality_metrics_ranking(self):
        composite_results = self.analytics.compute_composite_centrality()
        self.assertIn("person-rakesh", composite_results)

        # Rakesh Kumar should be identified as top hub / Possible Central Network Entity
        rakesh_metrics = composite_results["person-rakesh"]
        self.assertGreater(rakesh_metrics["composite_centrality_score"], 0.40)
        self.assertIn("Central Network Entity", rakesh_metrics["investigative_observation"])

        # Check betweenness centrality
        bet = self.analytics.compute_betweenness_centrality()
        self.assertGreater(bet["person-rakesh"], 0.20)

    def test_shortest_pathfinding(self):
        path = self.clustering.find_shortest_path("person-rakesh", "loc-singhu-border")
        self.assertIsNotNone(path)
        self.assertGreaterEqual(len(path), 3)

        # Start should be person-rakesh, end should be loc-singhu-border
        self.assertEqual(path[0]["node"]["id"], "person-rakesh")
        self.assertEqual(path[-1]["node"]["id"], "loc-singhu-border")

    def test_community_detection(self):
        communities = self.clustering.detect_communities_lpa()
        self.assertEqual(len(communities), len(self.graph.nodes))
        summary = self.clustering.get_clusters_summary()
        self.assertGreater(len(summary), 0)

    def test_investigative_terminology_guardrail(self):
        """Ensure no analytical outputs declare guilt or legal verdicts."""
        all_metrics = self.analytics.compute_composite_centrality()
        for node_id, data in all_metrics.items():
            obs = data["investigative_observation"].lower()
            self.assertNotIn("guilty", obs)
            self.assertNotIn("convicted", obs)
            self.assertNotIn("criminal", obs)


if __name__ == "__main__":
    unittest.main()
