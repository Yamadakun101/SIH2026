"""
Centrality Analytics Engine
Computes PageRank, Betweenness Centrality, Degree Centrality, and Key Network Hub indicators.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Tuple
from .graph_builder import CrimeGraph


class CentralityAnalytics:
    """Computes mathematical network centrality metrics to surface key facilitators and hubs."""

    def __init__(self, graph: CrimeGraph):
        self.graph = graph

    def compute_degree_centrality(self) -> Dict[str, float]:
        """Compute normalized degree centrality: deg(v) / (N - 1)."""
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        if n <= 1:
            return {node: 1.0 for node in nodes}

        centrality = {}
        for node in nodes:
            deg = len(self.graph.adjacency.get(node, set()))
            centrality[node] = round(deg / (n - 1), 4)
        return centrality

    def compute_betweenness_centrality(self) -> Dict[str, float]:
        """
        Compute betweenness centrality using Brandes' algorithm for unweighted graphs.
        Identifies bridge nodes that control flow between disparate parts of the network.
        """
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        if n <= 2:
            return {node: 0.0 for node in nodes}

        cb = {node: 0.0 for node in nodes}

        for s in nodes:
            # Single-source shortest paths (BFS)
            stack: List[str] = []
            pred: Dict[str, List[str]] = {w: [] for w in nodes}
            sigma = {w: 0 for w in nodes}
            sigma[s] = 1
            dist = {w: -1 for w in nodes}
            dist[s] = 0

            q = deque([s])
            while q:
                v = q.popleft()
                stack.append(v)
                for w in self.graph.adjacency.get(v, set()):
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        q.append(w)
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        pred[w].append(v)

            # Accumulate dependencies
            delta = {w: 0.0 for w in nodes}
            while stack:
                w = stack.pop()
                for v in pred[w]:
                    if sigma[w] > 0:
                        delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
                if w != s:
                    cb[w] += delta[w]

        # Normalization for undirected graph: 2 / ((n-1)(n-2))
        scale = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
        normalized_cb = {node: round(cb[node] * scale, 4) for node in nodes}
        return normalized_cb

    def compute_pagerank(
        self,
        damping: float = 0.85,
        max_iter: int = 100,
        tol: float = 1e-6
    ) -> Dict[str, float]:
        """Compute PageRank scores using power iteration."""
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        if n == 0:
            return {}
        if n == 1:
            return {nodes[0]: 1.0}

        ranks = {node: 1.0 / n for node in nodes}

        for _ in range(max_iter):
            next_ranks = {node: (1.0 - damping) / n for node in nodes}

            # Account for dangling nodes or standard undirected neighbor shares
            for node in nodes:
                neighbors = list(self.graph.adjacency.get(node, set()))
                deg = len(neighbors)
                if deg > 0:
                    share = damping * ranks[node] / deg
                    for neighbor in neighbors:
                        next_ranks[neighbor] += share
                else:
                    for other in nodes:
                        next_ranks[other] += damping * ranks[node] / n

            # Check convergence
            diff = sum(abs(next_ranks[node] - ranks[node]) for node in nodes)
            ranks = next_ranks
            if diff < tol:
                break

        # Normalize so maximum value is 1.0 or sum to 1
        max_val = max(ranks.values()) if ranks else 1.0
        return {node: round(ranks[node] / max_val, 4) for node in nodes}

    def compute_closeness_centrality(self) -> Dict[str, float]:
        """Compute closeness centrality: (n - 1) / sum(d(v, u))."""
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        if n <= 1:
            return {node: 1.0 for node in nodes}

        closeness = {}
        for s in nodes:
            dist = {w: -1 for w in nodes}
            dist[s] = 0
            q = deque([s])
            while q:
                v = q.popleft()
                for w in self.graph.adjacency.get(v, set()):
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        q.append(w)

            reachable_distances = [dist[w] for w in nodes if dist[w] > 0]
            if reachable_distances:
                sum_dist = sum(reachable_distances)
                closeness[s] = round(len(reachable_distances) / sum_dist, 4)
            else:
                closeness[s] = 0.0

        return closeness

    def compute_composite_centrality(self) -> Dict[str, Dict[str, Any]]:
        """
        Computes all centrality metrics and calculates a weighted composite score.
        Surfaces Investigative Leads without drawing legal conclusions.
        """
        deg = self.compute_degree_centrality()
        bet = self.compute_betweenness_centrality()
        pr = self.compute_pagerank()
        close = self.compute_closeness_centrality()

        results = {}
        for node_id, node in self.graph.nodes.items():
            d = deg.get(node_id, 0.0)
            b = bet.get(node_id, 0.0)
            p = pr.get(node_id, 0.0)
            c = close.get(node_id, 0.0)

            # Weighted composite score emphasizing Betweenness (facilitator hub) and PageRank
            composite = round((0.40 * b) + (0.30 * p) + (0.20 * d) + (0.10 * c), 3)

            is_high_centrality = composite >= 0.60
            investigative_label = (
                "Possible Central Network Entity" if is_high_centrality
                else "Key Peripheral / Associate Node" if composite >= 0.35
                else "Incidental / Search Subject Node"
            )

            results[node_id] = {
                "node_id": node_id,
                "label": node.label,
                "type": node.node_type,
                "degree_centrality": d,
                "betweenness_centrality": b,
                "pagerank_score": p,
                "closeness_centrality": c,
                "composite_centrality_score": composite,
                "investigative_observation": investigative_label,
            }

        return results

    def apply_centrality_to_graph(self) -> None:
        """Update node centrality_score fields in place on the graph."""
        composite_data = self.compute_composite_centrality()
        for node_id, data in composite_data.items():
            if node_id in self.graph.nodes:
                self.graph.nodes[node_id].centrality_score = data["composite_centrality_score"]

    def get_top_hub_entities(self, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return the top-K highest centrality entities in the network."""
        all_metrics = self.compute_composite_centrality()
        sorted_nodes = sorted(
            all_metrics.values(),
            key=lambda x: x["composite_centrality_score"],
            reverse=True
        )
        return sorted_nodes[:top_k]
