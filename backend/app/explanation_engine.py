from typing import Dict, List

def generate_explanation(acc: str, risk_data: Dict, patterns: List[str], graph_intelligence: Dict) -> str:
    """
    Generates a concise, audit-ready explanation for why an account was flagged.
    """
    score = risk_data["score"]
    breakdown = risk_data["breakdown"]
    
    triggers = []
    if breakdown["pattern_risk"] > 0.5:
        pattern_names = ", ".join(set(patterns))
        triggers.append(f"matched known fraud patterns ({pattern_names})")
        
    if breakdown["graph_risk"] > 0.6:
        is_hub = acc in graph_intelligence.get("hubs", [])
        role = "highly connected hub" if is_hub else "critical bridge"
        triggers.append(f"acts as a {role} in the transaction network")
        
    if breakdown["anomaly_score"] > 0.7:
        triggers.append("exhibits statistically high behavioral outliers compared to peers")
        
    if breakdown["velocity_risk"] > 0.5:
        triggers.append("showed a significant spike in transaction frequency recently")

    if not triggers:
        return f"Account flagged with a risk score of {score} based on low-level structural and behavioral anomalies."

    explanation = f"Account flagged ({score}/100) because it " + " and ".join(triggers[:2]) + "."
    if len(triggers) > 2:
        explanation += f" Additionally, it {triggers[2]}."
        
    return explanation

def batch_explain(final_scores: Dict, account_patterns: Dict, graph_intelligence: Dict) -> Dict:
    explanations = {}
    for acc, data in final_scores.items():
        if data["score"] > 20: # Only explain accounts with meaningful risk
            patterns = account_patterns.get(acc, ["general anomaly"])
            explanations[acc] = generate_explanation(acc, data, patterns, graph_intelligence)
    return explanations
