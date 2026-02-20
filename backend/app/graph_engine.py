import networkx as nx
import community as community_louvain
import pandas as pd

def build_graph(df: pd.DataFrame) -> nx.DiGraph:
    """
    Builds a directed graph from transaction data.
    Uses vectorized operations for speed.
    """
    G = nx.DiGraph()
    
    # Aggregating transactions between same pairs for performance
    edges_df = df.groupby(["sender_id", "receiver_id"]).agg({
        "amount": "sum",
        "transaction_id": "count"
    }).reset_index()
    
    for _, row in edges_df.iterrows():
        G.add_edge(
            row["sender_id"],
            row["receiver_id"],
            amount=row["amount"],
            weight=row["transaction_id"] # Use count as weight for centrality
        )
    return G

def analyze_graph_intelligence(G: nx.DiGraph):
    """
    Performs advanced graph analysis: Louvain communities, SCC, and Centrality.
    """
    if len(G) == 0:
        return {"communities": {}, "scc": [], "centrality": {"betweenness": {}, "pagerank": {}}, "hubs": []}

    # 1. Community Detection (Louvain) - Requires undirected graph
    undirected_G = G.to_undirected()
    communities = community_louvain.best_partition(undirected_G)
    
    # 2. Strongly Connected Components (DiGraph) - Finds cycles/loops
    scc = [list(c) for c in nx.strongly_connected_components(G) if len(c) > 1]
    
    # 3. Centrality Metrics
    # Betweenness finds "bridges" between communities
    betweenness = nx.betweenness_centrality(G, weight='weight')
    # PageRank finds influential/hub accounts
    pagerank = nx.pagerank(G, weight='amount')
    
    # Hub Detection (Nodes significantly above average centrality)
    avg_bt = sum(betweenness.values()) / len(betweenness) if betweenness else 0
    hubs = [node for node, bt in betweenness.items() if bt > avg_bt * 5]

    return {
        "communities": communities,
        "scc": scc,
        "centrality": {
            "betweenness": betweenness,
            "pagerank": pagerank
        },
        "hubs": hubs
    }
