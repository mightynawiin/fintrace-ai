import pandas as pd
import networkx as nx
from typing import List, Dict

def detect_shell_networks(G: nx.DiGraph, df: pd.DataFrame) -> List[Dict]:
    """
    Detects multi-hop laundering patterns (A -> B -> C -> D).
    Focuses on 'pass-through' accounts with low retention and high velocity.
    """
    shell_rings = []
    ring_counter = 1
    
    # 1. Identify potential pass-through nodes
    # Criteria: In-degree > 0 AND Out-degree > 0 AND low retention
    potential_mules = []
    
    # Pre-calculate in/out sums for performance
    in_sums = df.groupby("receiver_id")["amount"].sum()
    out_sums = df.groupby("sender_id")["amount"].sum()
    
    for node in G.nodes():
        if node in in_sums and node in out_sums:
            received = in_sums[node]
            sent = out_sums[node]
            
            # If retention is low (sent ~ received) and count is high
            retention_ratio = abs(received - sent) / max(received, 1)
            if retention_ratio < 0.15: # Retains less than 15%
                potential_mules.append(node)
    
    # 2. Find paths through these mules
    # We look for simple paths in the graph where intermediate nodes are in potential_mules
    paths = []
    for source in G.nodes():
        # Limit search depth for performance (max 4 hops as per AML standards)
        for target in G.nodes():
            if source == target: continue
            
            # Find paths of length 3+
            for path in nx.all_simple_paths(G, source, target, cutoff=4):
                if len(path) >= 4:
                    # Check if intermediate nodes are 'mules'
                    intermediates = path[1:-1]
                    if all(m in potential_mules for m in intermediates):
                        paths.append(path)

    # 3. Time Window Analysis on paths
    # Laundering often happens quickly
    for path in paths:
        # Check if timestamps are cascading
        path_txns = []
        valid_path = True
        
        last_time = None
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            # Get earliest transaction between u and v
            tx = df[(df["sender_id"] == u) & (df["receiver_id"] == v)].sort_values("timestamp").iloc[0]
            
            if last_time and tx["timestamp"] < last_time:
                valid_path = False
                break
            
            # Check elapsed time (should be within 48h for entire chain)
            if last_time and (tx["timestamp"] - first_time).total_seconds() > 172800:
                valid_path = False
                break
                
            if i == 0:
                first_time = tx["timestamp"]
            last_time = tx["timestamp"]
            
        if valid_path:
            shell_rings.append({
                "ring_id": f"RING_SHELL_{ring_counter:03d}",
                "pattern_type": "layered_shell",
                "member_accounts": path,
                "layering_depth": len(path) - 1,
                "risk_score": 0.85 # Base risk for validated shell path
            })
            ring_counter += 1
            
    # Deduplicate paths (keep longest)
    unique_rings = []
    sorted_shells = sorted(shell_rings, key=lambda x: len(x["member_accounts"]), reverse=True)
    seen_nodes = set()
    for ring in sorted_shells:
        members = set(ring["member_accounts"])
        if not (members & seen_nodes):
            unique_rings.append(ring)
            seen_nodes.update(members)
            
    return unique_rings
