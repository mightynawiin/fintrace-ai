import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(df: pd.DataFrame, G) -> pd.DataFrame:
    """
    Uses Isolation Forest to detect statistical outliers in transaction behavior.
    Features: Frequency, Avg Amount, In/Out Ratio, Connectivity.
    """
    # 1. Feature Engineering per Account
    send_stats = df.groupby("sender_id").agg({
        "amount": ["count", "mean", "std", "sum"],
    })
    send_stats.columns = ["out_count", "out_avg", "out_std", "out_sum"]
    
    recv_stats = df.groupby("receiver_id").agg({
        "amount": ["count", "mean", "std", "sum"],
    })
    recv_stats.columns = ["in_count", "in_avg", "in_std", "in_sum"]
    
    # Merge stats
    accounts = list(set(df["sender_id"]) | set(df["receiver_id"]))
    features = pd.DataFrame(index=accounts)
    features = features.join(send_stats).join(recv_stats).fillna(0)
    
    # Add engineered features
    features["in_out_ratio"] = (features["in_sum"] + 1) / (features["out_sum"] + 1)
    
    # Add graph features (degree)
    features["degree"] = [G.degree(acc) if acc in G else 0 for acc in features.index]
    
    # 2. Preprocessing
    # Handle NaN and Infinity
    features = features.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # 3. Isolation Forest
    # contamination is estimated % of outliers
    iso = IsolationForest(contamination=0.08, random_state=42)
    predictions = iso.fit_predict(scaled_features)
    # Convert predictions: -1 is outlier, 1 is normal -> convert to score 0-1
    # decision_function gives score (lower is more anomalous)
    anomaly_scores = iso.decision_function(scaled_features)
    
    # Normalize anomaly score to 0-1 range (1 = most anomalous)
    min_score = anomaly_scores.min()
    max_score = anomaly_scores.max()
    normalized_scores = (anomaly_scores - max_score) / (min_score - max_score) if max_score != min_score else np.zeros_like(anomaly_scores)
    
    results = pd.DataFrame({
        "anomaly_score": normalized_scores
    }, index=features.index)
    
    return results
