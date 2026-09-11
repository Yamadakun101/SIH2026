"""
Syndicate Clustering & Pathfinding Analytics
Detects sub-network communities and traces multi-hop suspicious connection paths.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Set
from .graph_builder import CrimeGraph


class SyndicateClustering:
    """Community detection and connection pathfinding for criminal network intelligence."""

    def __init__(self, graph: CrimeGraph):
        self.graph = graph

    def detect_communities_lpa(self, max_iter: int = 20) -> Dict[str, int]:
        """
        Label Propagation Algorithm (LPA) to partition the network into clusters/syndicates.
        Returns a mapping of node_id -> cluster_id (int).
        """
        nodes = list(self.graph.nodes.keys())
        if not nodes:
            return {}

        # Initialize each node with unique label
        labels = {node: i for i, node in enumerate(nodes)}

        for _ in range(max_iter):
            changed = False
            for node in nodes:
                neighbors = list(self.graph.adjacency.get(node, set()))
                if not neighbors:
                    continue

                # Count label frequencies among neighbors
                label_counts: Dict[int, int] = {}
                for neighbor in neighbors:
                    lbl = labels[neighbor]
                    label_counts[lbl] = label_counts.get(lbl, 0) + 1

                max_freq = max(label_counts.values())
                # Pick the smallest label with maximum frequency deterministically
                best_label = min(lbl for lbl, count in label_counts.items() if count == max_freq)

                if best_label != labels[node]:
                    labels[node] = best_label
                    changed = True

            if not changed:
                break

        # Normalize cluster IDs from 0 to K-1
        unique_labels = sorted(list(set(labels.values())))
        label_map = {old: new for new, old in enumerate(unique_labels)}
        return {node: label_map[lbl] for node, lbl in labels.items()}

    def get_clusters_summary(self) -> List[Dict[str, Any]]:
        """Get structured summary of detected clusters/syndicates."""
        communities = self.detect_communities_lpa()
        clusters: Dict[int, List[str]] = {}
        for node, cid in communities.items():
            clusters.setdefault(cid, []).append(node)

        summary = []
        for cid, member_ids in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
            members = [
                {
                    "id": nid,
                    "label": self.graph.nodes[nid].label,
                    "type": self.graph.nodes[nid].node_type,
                    "centrality": self.graph.nodes[nid].centrality_score,
                }
                for nid in member_ids
                if nid in self.graph.nodes
            ]
            summary.append({
                "cluster_id": cid,
                "cluster_name": f"Sub-Network Group #{cid + 1}",
                "size": len(members),
                "members": members,
            })
        return summary

    def find_shortest_path(self, start_id: str, end_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Find shortest path between two nodes using BFS.
        Returns list of path segments with node details and connecting edges.
        """
        if start_id not in self.graph.nodes or end_id not in self.graph.nodes:
            return None
        if start_id == end_id:
            return [{"node": self.graph.nodes[start_id].to_dict()}]

        visited: Set[str] = {start_id}
        queue = deque([(start_id, [start_id])])

        shortest_path_nodes: Optional[List[str]] = None
        while queue:
            current, path = queue.popleft()
            if current == end_id:
                shortest_path_nodes = path
                break

            for neighbor in self.graph.adjacency.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        if not shortest_path_nodes:
            return None

        # Build detailed step-by-step path
        path_details = []
        for i, nid in enumerate(shortest_path_nodes):
            step: Dict[str, Any] = {"node": self.graph.nodes[nid].to_dict()}
            if i < len(shortest_path_nodes) - 1:
                next_nid = shortest_path_nodes[i + 1]
                # Find connecting edge
                connecting_edge = None
                for e in self.graph.edges.values():
                    if (e.source == nid and e.target == next_nid) or (e.source == next_nid and e.target == nid):
                        connecting_edge = e.to_dict()
                        break
                step["via_edge"] = connecting_edge
            path_details.append(step)

        return path_details

    def find_all_paths(self, start_id: str, end_id: str, max_depth: int = 4) -> List[List[str]]:
        """Find all simple connection paths between start and end within max_depth."""
        if start_id not in self.graph.nodes or end_id not in self.graph.nodes:
            return []

        all_paths: List[List[str]] = []

        def dfs(curr: str, target: str, visited: Set[str], current_path: List[str]):
            if len(current_path) > max_depth + 1:
                return
            if curr == target:
                all_paths.append(list(current_path))
                return

            for neighbor in self.graph.adjacency.get(curr, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor, target, visited, current_path + [neighbor])
                    visited.remove(neighbor)

        dfs(start_id, end_id, {start_id}, [start_id])
        return all_paths

    def find_common_associates(self, node_id_1: str, node_id_2: str) -> List[Dict[str, Any]]:
        """Find shared neighbor entities connected to both nodes."""
        n1_neighbors = set(self.graph.get_neighbors(node_id_1))
        n2_neighbors = set(self.graph.get_neighbors(node_id_2))
        shared_ids = n1_neighbors.intersection(n2_neighbors)

        return [
            self.graph.nodes[nid].to_dict()
            for nid in shared_ids
            if nid in self.graph.nodes
        ]
