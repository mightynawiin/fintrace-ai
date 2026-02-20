# backend/app/smurf_detector.py

from datetime import timedelta
import numpy as np

WINDOW_HOURS = 72
MIN_UNIQUE_ACCOUNTS = 10
MIN_TOTAL_AMOUNT = 5000
MAX_AMOUNT_STD = 5000


def detect_smurfing(df):
    rings = []
    ring_counter = 1

    df_sorted = df.sort_values("timestamp")

    # -------------------------
    # FAN-IN (Many -> One)
    # -------------------------
    grouped_receiver = df_sorted.groupby("receiver_id")

    for receiver, group in grouped_receiver:
        group = group.sort_values("timestamp").reset_index(drop=True)

        start = 0
        for end in range(len(group)):

            # Sliding 72h window
            while (
                group.loc[end, "timestamp"]
                - group.loc[start, "timestamp"]
            ).total_seconds() > WINDOW_HOURS * 3600:
                start += 1

            window = group.loc[start:end]
            unique_senders = window["sender_id"].unique()

            if len(unique_senders) >= MIN_UNIQUE_ACCOUNTS:

                # ✅ Additional Intelligence Checks

                total_amount = window["amount"].sum()
                amount_std = window["amount"].std()

                # Check if receiver redistributes funds (true mule behavior)
                outgoing_txns = df_sorted[df_sorted["sender_id"] == receiver]
                outgoing_count = len(outgoing_txns)

                if (
                    total_amount >= MIN_TOTAL_AMOUNT and
                    outgoing_count > 0 and
                    (amount_std is not None and amount_std < MAX_AMOUNT_STD)
                ):

                    ring_id = f"RING_SMURF_IN_{ring_counter:03d}"

                    rings.append({
                        "ring_id": ring_id,
                        "pattern_type": "fan_in_72h",
                        "member_accounts": list(unique_senders) + [receiver]
                    })

                    ring_counter += 1
                    break  # avoid duplicates for same receiver

    # -------------------------
    # FAN-OUT (One -> Many)
    # -------------------------
    grouped_sender = df_sorted.groupby("sender_id")

    for sender, group in grouped_sender:
        group = group.sort_values("timestamp").reset_index(drop=True)

        start = 0
        for end in range(len(group)):

            while (
                group.loc[end, "timestamp"]
                - group.loc[start, "timestamp"]
            ).total_seconds() > WINDOW_HOURS * 3600:
                start += 1

            window = group.loc[start:end]
            unique_receivers = window["receiver_id"].unique()

            if len(unique_receivers) >= MIN_UNIQUE_ACCOUNTS:

                total_amount = window["amount"].sum()
                amount_std = window["amount"].std()

                if (
                    total_amount >= MIN_TOTAL_AMOUNT and
                    (amount_std is not None and amount_std < MAX_AMOUNT_STD)
                ):

                    ring_id = f"RING_SMURF_OUT_{ring_counter:03d}"

                    rings.append({
                        "ring_id": ring_id,
                        "pattern_type": "fan_out_72h",
                        "member_accounts": [sender] + list(unique_receivers)
                    })

                    ring_counter += 1
                    break

    return rings
