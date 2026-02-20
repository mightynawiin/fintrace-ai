import pandas as pd
import numpy as np
from typing import Dict, List

def calculate_final_scores(
    accounts: List[str],
    graph_intelligence: Dict,
    anomaly_results: pd.DataFrame,
    pattern_rings: List[Dict],
    df: pd.DataFrame
) -> Dict:
    """
    Weighted Risk Model:
    40% Graph Structure | 30% Anomaly Score | 20% Pattern Severity | 10% Velocity
    """
    final_scores = {}
    
    # Pre-parse patterns for lookup
    account_patterns = {}
    for ring in pattern_rings:
        for acc in ring["member_accounts"]:
            if acc not in account_patterns:
                account_patterns[acc] = []
            account_patterns[acc].append(ring["pattern_type"])

    # Graph metrics
    bt = graph_intelligence["centrality"]["betweenness"]
    pr = graph_intelligence["centrality"]["pagerank"]
    hubs = set(graph_intelligence["hubs"])
    
    # Velocity calculation (spike in last 24h of data)
    max_time = df["timestamp"].max()
    spike_window = df[df["timestamp"] > (max_time - pd.Timedelta(hours=24))]
    spikes = spike_window.groupby("sender_id").size().to_dict()

    for acc in accounts:
        # 1. Graph Structure Risk (0-1)
        # Combination of centrality and hub status
        g_risk = (bt.get(acc, 0) * 0.5 + pr.get(acc, 0) * 0.5)
        if acc in hubs: g_risk = max(g_risk, 0.8)
        g_risk = min(g_risk * 10, 1.0) # Scale up
        
        # 2. Anomaly Score (0-1)
        a_risk = anomaly_results.loc[acc, "anomaly_score"] if acc in anomaly_results.index else 0
        
        # 3. Pattern Severity (0-1)
        patterns = account_patterns.get(acc, [])
        p_risk = 0
        if "layered_shell" in patterns: p_risk = 0.9
        elif any("cycle" in p for p in patterns): p_risk = 0.7
        elif any("fan" in p for p in patterns): p_risk = 0.6
        elif patterns: p_risk = 0.4
        
        # 4. Velocity Spike (0-1)
        v_count = spikes.get(acc, 0)
        v_risk = min(v_count / 20, 1.0) # 20+ txns in 24h is high risk
        
        # WEIGHTED CALCULATION
        raw_score = (
            (g_risk * 0.4) +
            (a_risk * 0.3) +
            (p_risk * 0.2) +
            (v_risk * 0.1)
        )
        
        # Normalize to 0-100
        final_score = round(raw_score * 100, 2)
        
        # Confidence score (How much data do we have for this account?)
        total_txns = len(df[(df["sender_id"] == acc) | (df["receiver_id"] == acc)])
        confidence = min(total_txns / 5, 1.0) # Need 5+ txns for high confidence
        
        final_scores[acc] = {
            "score": final_score,
            "confidence": round(confidence, 2),
            "breakdown": {
                "graph_risk": round(g_risk, 2),
                "anomaly_score": round(a_risk, 2),
                "pattern_risk": round(p_risk, 2),
                "velocity_risk": round(v_risk, 2)
            }
        }
        
    return final_scores
