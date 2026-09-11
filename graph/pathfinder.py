"""
Pathfinder & Flow-Tracing Analytics Engine
Traces shortest paths, suspicious flow paths, and multi-hop connections between entities.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Set
from .graph_builder import CrimeGraph


class CrimePathFinder:
    """Computes investigative flow tracing and shortest paths between case entities."""

    def __init__(self, graph: CrimeGraph):
        self.graph = graph

    def find_shortest_path(self, start_id: str, end_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Find shortest path between two nodes using Breadth-First Search (BFS).
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
                connecting_edge = None
                for e in self.graph.edges.values():
                    if (e.source == nid and e.target == next_nid) or (e.source == next_nid and e.target == nid):
                        connecting_edge = e.to_dict()
                        break
                step["via_edge"] = connecting_edge
            path_details.append(step)

        return path_details

    def trace_flow_to_mule_accounts(self, start_suspect_id: str) -> List[Dict[str, Any]]:
        """Trace all paths from a suspect node to known financial mule accounts."""
        mule_nodes = [
            nid for nid, n in self.graph.nodes.items()
            if n.node_type == "BANK_ACCOUNT" or "MULE" in (n.sub_role or "").upper()
        ]

        flows = []
        for mule_id in mule_nodes:
            path = self.find_shortest_path(start_suspect_id, mule_id)
            if path:
                flows.append({
                    "target_account_id": mule_id,
                    "target_label": self.graph.nodes[mule_id].label,
                    "hops": len(path) - 1,
                    "path_details": path
                })
        return flows
