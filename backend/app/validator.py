# backend/app/validator.py

import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "sender_id",
    "receiver_id",
    "amount",
    "timestamp"
]

def validate_csv(df: pd.DataFrame):
    # Check exact columns
    if list(df.columns) != REQUIRED_COLUMNS:
        raise ValueError(
            f"Invalid CSV format. Required columns EXACTLY: {REQUIRED_COLUMNS}"
        )

    # Validate types
    df["transaction_id"] = df["transaction_id"].astype(str)
    df["sender_id"] = df["sender_id"].astype(str)
    df["receiver_id"] = df["receiver_id"].astype(str)
    df["amount"] = df["amount"].astype(float)

    # Strict timestamp format
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="%Y-%m-%d %H:%M:%S",
        errors="raise"
    )

    return df
