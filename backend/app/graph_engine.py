import networkx as nx
from typing import Dict, List, Any, Optional
from .data_store import INITIAL_NODES, INITIAL_EDGES
import copy

class CriminalGraphEngine:
    def __init__(self):
        self.nodes = copy.deepcopy(INITIAL_NODES)
        self.edges = copy.deepcopy(INITIAL_EDGES)
        self.G = nx.Graph()
        self.build_graph()

    def build_graph(self):
        self.G.clear()
        for node in self.nodes:
            self.G.add_node(
                node["id"],
                label=node["label"],
                type=node["type"],
                risk_score=node.get("risk_score", 50.0),
                syndicate=node.get("syndicate", "Unknown"),
                metadata=node.get("metadata", {})
            )
        for edge in self.edges:
            self.G.add_edge(
                edge["source"],
                edge["target"],
                id=edge["id"],
                type=edge["type"],
                weight=edge.get("weight", 1.0),
                frequency=edge.get("frequency", 1),
                evidence_count=edge.get("evidence_count", 1),
                label=edge.get("label", edge["type"]),
                metadata=edge.get("metadata", {})
            )

    def compute_centralities(self) -> Dict[str, Dict[str, float]]:
        """
        Calculates key criminal intelligence metrics:
        - Degree Centrality: Connection density
        - Betweenness Centrality: Kingpin / Broker / Conduit identification
        - PageRank: Syndicate influence / Authority
        """
        if len(self.G) == 0:
            return {}

        degree = nx.degree_centrality(self.G)
        betweenness = nx.betweenness_centrality(self.G, weight="weight")
        try:
            pagerank = nx.pagerank(self.G, weight="weight")
        except Exception:
            pagerank = {n: 1.0 / len(self.G) for n in self.G.nodes()}

        centralities = {}
        for n in self.G.nodes():
            centralities[n] = {
                "degree": round(degree.get(n, 0.0), 4),
                "betweenness": round(betweenness.get(n, 0.0), 4),
                "pagerank": round(pagerank.get(n, 0.0), 4),
                # Kingpin Index combines betweenness, pagerank, and entity risk score
                "kingpin_index": round((betweenness.get(n, 0.0) * 0.45 + pagerank.get(n, 0.0) * 0.35 + (self.G.nodes[n].get("risk_score", 50) / 100.0) * 0.20) * 100, 2)
            }
        return centralities

    def detect_communities(self) -> Dict[str, int]:
        """
        Detects criminal syndicates / sub-gangs using modularity community detection
        """
        try:
            communities = list(nx.community.greedy_modularity_communities(self.G))
            comm_map = {}
            for idx, comm in enumerate(communities):
                for node_id in comm:
                    comm_map[node_id] = idx + 1
            return comm_map
        except Exception:
            return {n: 1 for n in self.G.nodes()}

    def get_full_graph_data(self) -> Dict[str, Any]:
        centralities = self.compute_centralities()
        communities = self.detect_communities()

        enriched_nodes = []
        for n in self.nodes:
            n_copy = copy.deepcopy(n)
            n_id = n_copy["id"]
            if n_id in centralities:
                n_copy["centrality"] = centralities[n_id]
                n_copy["community_id"] = communities.get(n_id, 1)
            enriched_nodes.append(n_copy)

        # Graph summary statistics
        summary = {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "suspects_count": sum(1 for n in self.nodes if n["type"] == "person"),
            "phones_tracked": sum(1 for n in self.nodes if n["type"] == "phone"),
            "vehicles_monitored": sum(1 for n in self.nodes if n["type"] == "vehicle"),
            "bank_accounts_flagged": sum(1 for n in self.nodes if n["type"] == "account"),
            "cctv_nodes": sum(1 for n in self.nodes if n["type"] == "cctv"),
            "organizations": sum(1 for n in self.nodes if n["type"] == "organization"),
            "locations": sum(1 for n in self.nodes if n["type"] == "location"),
            "density": round(nx.density(self.G), 4) if len(self.G) > 0 else 0,
            "connected_components": nx.number_connected_components(self.G) if len(self.G) > 0 else 0
        }

        # Identify top 5 Kingpins / Conduits by Kingpin Index
        sorted_by_kingpin = sorted(
            [n for n in enriched_nodes if n.get("type") == "person"],
            key=lambda x: x.get("centrality", {}).get("kingpin_index", 0),
            reverse=True
        )
        summary["top_kingpins"] = [
            {
                "id": k["id"],
                "name": k["label"],
                "alias": k["metadata"].get("alias", ""),
                "role": k["metadata"].get("role", ""),
                "syndicate": k.get("syndicate", ""),
                "kingpin_index": k.get("centrality", {}).get("kingpin_index", 0),
                "risk_score": k.get("risk_score", 0)
            }
            for k in sorted_by_kingpin[:4]
        ]

        return {
            "nodes": enriched_nodes,
            "edges": self.edges,
            "summary": summary
        }

    def find_shortest_path(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """
        Discovers the shortest criminal linkage chain between any two entities
        """
        if not self.G.has_node(source_id) or not self.G.has_node(target_id):
            return {"found": False, "message": "Source or target node not found in graph."}

        try:
            path_nodes = nx.shortest_path(self.G, source=source_id, target=target_id)
            path_edges = []
            for i in range(len(path_nodes) - 1):
                u, v = path_nodes[i], path_nodes[i + 1]
                edge_data = self.G.get_edge_data(u, v)
                path_edges.append({
                    "source": u,
                    "target": v,
                    "type": edge_data.get("type"),
                    "label": edge_data.get("label"),
                    "metadata": edge_data.get("metadata", {})
                })

            detailed_nodes = [self.get_node_by_id(n_id) for n_id in path_nodes]
            return {
                "found": True,
                "length": len(path_nodes) - 1,
                "path_node_ids": path_nodes,
                "nodes": detailed_nodes,
                "edges": path_edges
            }
        except nx.NetworkXNoPath:
            return {"found": False, "message": f"No connected pathway exists between {source_id} and {target_id}."}

    def get_node_by_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        for n in self.nodes:
            if n["id"] == node_id:
                return n
        return None

    def add_node(self, node_dict: Dict[str, Any]):
        # check if exists
        for idx, n in enumerate(self.nodes):
            if n["id"] == node_dict["id"]:
                self.nodes[idx] = node_dict
                self.build_graph()
                return
        self.nodes.append(node_dict)
        self.build_graph()

    def add_edge(self, edge_dict: Dict[str, Any]):
        for idx, e in enumerate(self.edges):
            if e["id"] == edge_dict["id"]:
                self.edges[idx] = edge_dict
                self.build_graph()
                return
        self.edges.append(edge_dict)
        self.build_graph()

# Singleton instance
graph_engine = CriminalGraphEngine()
