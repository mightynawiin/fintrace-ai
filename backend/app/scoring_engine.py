import networkx as nx
import numpy as np


def compute_suspicion_scores(G, df, rings):

    scores = {}

    pagerank = nx.pagerank(G)
    betweenness = nx.betweenness_centrality(G)

    for ring in rings:

        pattern = ring["pattern_type"]
        members = ring["member_accounts"]

        if pattern == "cycle":
            base_weight = 40
        elif pattern in ["fan_in", "fan_out"]:
            base_weight = 35
        elif pattern == "layered_shell":
            base_weight = 50
        else:
            base_weight = 20

        sub_df = df[
            (df["sender_id"].isin(members)) &
            (df["receiver_id"].isin(members))
        ]

        avg_amount = sub_df["amount"].mean()
        amount_score = min(avg_amount / 200, 20)

        timestamps = sub_df["timestamp"].sort_values()
        if len(timestamps) > 1:
            duration_hours = (
                (timestamps.iloc[-1] - timestamps.iloc[0]).total_seconds()
                / 3600
            )
            velocity_score = max(0, 15 - duration_hours)
        else:
            velocity_score = 5

        size_factor = len(members) * 2

        for member in members:

            centrality_score = (
                pagerank.get(member, 0) * 30 +
                betweenness.get(member, 0) * 30
            )

            final_score = (
                base_weight +
                centrality_score +
                amount_score +
                velocity_score +
                size_factor
            )

            scores[member] = min(round(final_score, 2), 100)

        ring["risk_score"] = round(
            np.mean([scores[m] for m in members]),
            2
        )

    return scores
